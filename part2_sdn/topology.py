#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI


CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 6633


def run():
    net = None

    try:
        net = Mininet(
            controller=None,
            switch=OVSKernelSwitch,
        )

        net.addController(
            "c0",
            controller=RemoteController,
            ip=CONTROLLER_IP,
            port=CONTROLLER_PORT,
        )

        s1 = net.addSwitch("s1", protocols="OpenFlow13")
        h1 = net.addHost("h1")
        h2 = net.addHost("h2")

        net.addLink(h1, s1)
        net.addLink(h2, s1)

        net.start()

        print("Nodes:", net.hosts, net.switches, net.controllers)
        print(f"Ryu controller: {CONTROLLER_IP}:{CONTROLLER_PORT}")
        print("Run 'pingall' at the Mininet prompt.")

        CLI(net)

    finally:
        if net is not None:
            net.stop()


if __name__ == "__main__":
    run()
