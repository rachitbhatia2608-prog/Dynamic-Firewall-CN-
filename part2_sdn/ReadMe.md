# Part 2: SDN Controller and Mininet Topology

## 1. Overview

This part demonstrates Software-Defined Networking (SDN) using the
Ryu controller, OpenFlow 1.3, Open vSwitch, and Mininet.

The Ryu application implements a learning switch. It learns source
MAC addresses and their associated switch ports, floods packets when
the destination is unknown, and installs forwarding flows for known
unicast traffic.

## 2. Project Structure

- `controller.py` - Ryu SDN controller application.
- `topology.py` - Creates the Mininet network containing one switch
  and two hosts.
- `README.md` - Documentation and execution instructions.

## 3. Requirements

The tested environment uses:

- Ubuntu 22.04
- Python 3
- Ryu 4.34 in the existing virtual environment
- Mininet 2.3.0
- Open vSwitch
- OpenFlow 1.3

Ryu virtual environment:

    /home/rachit/ryu/venv

## 4. Network Topology

The Mininet topology contains:

- One Open vSwitch: `s1`
- Two hosts: `h1` and `h2`
- One remote Ryu controller: `c0`

Both hosts connect to the same switch. The controller listens on
`127.0.0.1:6633`.

## 5. How to Run

Use two Ubuntu terminals.

### Terminal 1: Start the Ryu controller

    cd /home/rachit/CN-Dynamic-Firewall/part2_sdn
    source /home/rachit/ryu/venv/bin/activate
    ryu-manager --ofp-tcp-listen-port 6633 controller.py

Wait for Ryu to load the application and keep this terminal running.

### Terminal 2: Start Mininet

    cd /home/rachit/CN-Dynamic-Firewall/part2_sdn
    sudo python3 topology.py

When the `mininet>` prompt appears, the topology is running.

## 6. Test Connectivity

At the Mininet prompt, run:

    nodes
    pingall
    h1 ping -c 3 h2

The expected `pingall` result is:

    *** Results: 0% dropped (2/2 received)

Successful pings indicate that the hosts can communicate through
the switch under the Ryu controller.

## 7. Inspect OpenFlow Rules

At the Mininet prompt, run:

    sh ovs-ofctl -O OpenFlow13 dump-flows s1

The output should show a table-miss rule that sends unmatched
packets to the controller and learned unicast forwarding flows
for known source and destination MAC addresses.

## 8. Expected Controller Behaviour

- Learns source MAC addresses and switch ports.
- Floods traffic when the destination MAC address is unknown.
- Forwards traffic to a known destination port.
- Installs OpenFlow rules for known unicast traffic.
- Logs learning, flooding, and flow-installation events.

## 9. Verification

The topology was tested with `pingall` and a three-packet ping
from `h1` to `h2`. Both tests completed with zero packet loss.
The OpenFlow flow table showed learned forwarding rules.

## 10. Current Limitations

This implementation is a basic SDN learning switch. It does not
yet implement dynamic firewall policies, malicious-traffic detection,
or a dedicated security-event logger.

These features require additional implementation and testing before
the complete dynamic firewall project can be considered finished.

## 11. Cleanup

Exit the Mininet CLI by entering:

    exit

Stop the Ryu controller with Ctrl+C in its terminal.

If stale Mininet resources remain, run:

    sudo mn -c
