from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import (
    CONFIG_DISPATCHER,
    MAIN_DISPATCHER,
    set_ev_cls,
)
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Table-miss: send unmatched packets to the controller.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER,
            )
        ]
        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions,
            )
        ]
        datapath.send_msg(
            parser.OFPFlowMod(
                datapath=datapath,
                priority=0,
                match=match,
                instructions=instructions,
            )
        )

        self.logger.info(
            "Switch connected: dpid=%s; table-miss installed",
            datapath.id,
        )

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth is None:
            return

        # Ignore LLDP frames.
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        src = eth.src
        dst = eth.dst
        dpid = datapath.id

        # Learn source MAC -> ingress port for this switch.
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        self.logger.info(
            "Learned MAC %s on switch %s port %s",
            src, dpid, in_port,
        )

        # Forward to a known port, otherwise flood.
        out_port = self.mac_to_port[dpid].get(
            dst, ofproto.OFPP_FLOOD
        )
        actions = [parser.OFPActionOutput(out_port)]

        # Install a flow for known unicast traffic.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(
                in_port=in_port,
                eth_src=src,
                eth_dst=dst,
            )
            instructions = [
                parser.OFPInstructionActions(
                    ofproto.OFPIT_APPLY_ACTIONS,
                    actions,
                )
            ]

            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                datapath.send_msg(
                    parser.OFPFlowMod(
                        datapath=datapath,
                        buffer_id=msg.buffer_id,
                        priority=1,
                        match=match,
                        instructions=instructions,
                    )
                )
                self.logger.info(
                    "Installed flow %s -> %s via port %s",
                    src, dst, out_port,
                )
                return

            datapath.send_msg(
                parser.OFPFlowMod(
                    datapath=datapath,
                    priority=1,
                    match=match,
                    instructions=instructions,
                )
            )
            self.logger.info(
                "Installed flow %s -> %s via port %s",
                src, dst, out_port,
            )
        else:
            self.logger.info(
                "Unknown destination %s; flooding", dst
            )

        # Send the packet now. Include data when the switch did not
        # buffer the packet at the controller.
        data = (
            msg.data
            if msg.buffer_id == ofproto.OFP_NO_BUFFER
            else None
        )
        datapath.send_msg(
            parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=msg.buffer_id,
                in_port=in_port,
                actions=actions,
                data=data,
            )
        )
