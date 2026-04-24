# SDN-packet-drop-simulator-AM288

## Problem Statement
In traditional networks, traffic control is rigid and hardware-dependent. This project simulates a **Software Defined Network (SDN)** where a centralized POX controller selectively drops packets from a specific host (h1) while allowing all other traffic to flow normally. This demonstrates how SDN enables programmable, fine-grained traffic control using OpenFlow rules.

## Network Topology
- **1 Switch:** s1
- **3 Hosts:** h1, h2, h3 (all connected to s1)
- **Controller:** POX (remote, running on port 6633)

- h1 ─┐
  h2 ─┤── s1 ── [POX Controller]
  h3 ─┘

  ## Setup & Execution Steps

### Requirements
- Ubuntu (Linux)
- Mininet
- POX Controller
- Python 3

### Step 1: Clone the repository
```bash
git clone https://github.com/sriviswaja/SDN-packet-drop-simulator-AM288.git
cd SDN-packet-drop-simulator-AM288
```

### Step 2: Copy controller to POX directory
```bash
cp packet_drop.py ~/pox/
```

### Step 3: Start the POX controller
```bash
cd ~/pox
python3 pox.py log.level --DEBUG packet_drop
```

### Step 4: Start Mininet (in a new terminal)
```bash
sudo mn --topo single,3 --controller remote
```

### Step 5: Test traffic
```bash
mininet> h1 ping h2   # Should be BLOCKED (100% packet loss)
mininet> h2 ping h3   # Should WORK (0% packet loss)
```

## Expected Output

### h1 ping h2 — BLOCKED ❌
h1's traffic is dropped by the OpenFlow rule installed by the controller.
- 100% packet loss
- "Destination Host Unreachable"

### h2 ping h3 — ALLOWED ✅
Normal traffic flows between h2 and h3.
- 0% packet loss
- Response times ~0.05–86ms

## Flow Table (ovs-ofctl dump-flows s1)
The DROP rule for h1's MAC address is installed with priority 100:

priority=100, dl_src=62:06:d9:61:09:f7 actions=drop
dl_dst=ff:ff:ff:ff:ff:ff actions=FLOOD
dl_dst=22:d6:f4:40:66:d1 actions=output:"s1-eth2"
dl_dst=12:fa:20:7c:7a:ba actions=output:"s1-eth3"

## Proof of Execution
Screenshots are available in the `/images` folder:
- `topology.png` — Mininet topology setup
- `controller.png` — POX controller logs showing DROP rule installation
- `flow.png` — Flow table dump showing the drop rule
- `blocked_and_allowed_traffic.png` — Ping results showing h1 blocked, h2↔h3 allowed

## References
- [POX Controller Documentation](https://noxrepo.github.io/pox-doc/html/)
- [Mininet Documentation](http://mininet.org/documentation/)
- [OpenFlow Specification](https://opennetworking.org/sdn-resources/openflow/)
