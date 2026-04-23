from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr
from pox.lib.packet import ethernet

log = core.getLogger()
mac_to_port = {}

BLOCKED_MAC = "62:06:d9:61:09:f7"

def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid
    in_port = event.port

    mac_to_port.setdefault(dpid, {})
    src = packet.src
    dst = packet.dst
    mac_to_port[dpid][src] = in_port

    # Install a DROP flow rule for h1's MAC at the switch level
    if src == EthAddr(BLOCKED_MAC):
        log.info("Installing DROP rule for h1 (MAC: %s)" % BLOCKED_MAC)
        msg = of.ofp_flow_mod()
        msg.match.dl_src = EthAddr(BLOCKED_MAC)
        msg.priority = 100
        # No actions = DROP
        event.connection.send(msg)
        return  # Don't forward this packet either

    # Normal L2 learning switch behavior for others
    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_flow_mod()
    msg.match.dl_dst = dst
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # Also send current packet out
    pkt_out = of.ofp_packet_out()
    pkt_out.data = event.ofp
    pkt_out.actions.append(of.ofp_action_output(port=out_port))
    pkt_out.in_port = in_port
    event.connection.send(pkt_out)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Packet Drop Simulator launched. Will block MAC: %s" % BLOCKED_MAC)
