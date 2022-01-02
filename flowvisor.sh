#!/bin/bash

# Start FlowVisor service
echo "Starting FlowVisor service..."
sudo /etc/init.d/flowvisor start

echo "Waiting for service to start..."
sleep 10
echo "Done."

# Get FlowVisor current config
echo "FlowVisor initial config:"
fvctl -f /etc/flowvisor/flowvisor.passwd get-config

# Get FlowVisor current defined slices
echo "FlowVisor initially defined slices:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Get FlowVisor current defined flowspaces
echo "FlowVisor initially defined flowspaces:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

# Get FlowVisor connected switches
echo "FlowVisor connected switches:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-datapaths

# Get FlowVisor connected switches links up
echo "FlowVisor connected switches links:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-links

# Define the FlowVisor slices
echo "Definition of FlowVisor slices..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice office1 tcp:localhost:10001 admin@office1
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice office2 tcp:localhost:10002 admin@office2
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice controller tcp:localhost:10003 admin@controller
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice office3 tcp:localhost:10004 admin@office3
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice administration tcp:localhost:10005 admin@administration
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice it tcp:localhost:10006 admin@it

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
#Switch 1 VOIP
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-voip-dst-port1 1 100 tp_dst=5060 controller=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-voip-src-port1 1 100 tp_src=5060 controller=7

# Switch 1 FTP



#Switch 1 Other traffic

#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port1 1  controller=7


#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port2 1 1 in_port=2 controller=7
#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port3 1 1 in_port=3 controller=7
#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port4 1 1 in_port=4 controller=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 100 tp_dst=5060 office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 100 tp_src=5060 office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 100 tp_dst=5060 office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 100 tp_src=5060 office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 100 tp_dst=5060 office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 100 tp_src=5060 office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 100 tp_dst=5060 office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 100 tp_src=5060 office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 100 tp_dst=5060 office3=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 100 tp_src=5060 office3=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7 7 100 tp_dst=5060 it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7 7 100 tp_src=5060 it=7

# OTHER OFFICES PING
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1 1 1 any controller=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 1 any office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 1 any office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 1 any office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 6 1 any office3=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-arp 1 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-arp 2 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-arp 3 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-arp 4 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-arp 5 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-arp 6 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-arp 7 500 dl_type=2054  it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-administration-dst 1 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-administration-src 1 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-administration-dst 2 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-administration-src 2 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-administration-dst 3 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-administration-src 3 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-administration-dst 4 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-administration-src 4 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-administration-dst 5 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-administration-src 5 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-administration-dst 6 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-administration-src 6 100 tp_src=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-administration-dst 7 100 tp_dst=22 administration=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-administration-src 7 100 tp_src=22 administration=7

## IT FLOWSPACE 0c e 0d

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-it1 7 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-it2 7 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-it3 7 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7-it4 7 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-it1 6 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-it2 6 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-it3 6 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6-it4 6 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-it1 5 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-it2 5 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-it3 5 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5-it4 5 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-it1 4 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-it2 4 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-it3 4 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4-it4 4 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-it1 3 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-it2 3 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-it3 3 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-it4 3 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-it1 2 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-it2 2 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-it3 2 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-it4 2 200 eth_src=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-it1 1 200 eth_dst=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-it2 1 200 eth_src=00:00:00:00:00:0c it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-it3 1 200 eth_dst=00:00:00:00:00:0d it=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-it4 1 200 eth_src=00:00:00:00:00:0d it=7


# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace