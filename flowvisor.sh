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
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice voip tcp:localhost:10001 admin@voip
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice data tcp:localhost:10002 admin@data
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice controller tcp:localhost:10003 admin@controller

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-src 1 2 tp_src=9999 controller=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-dst 1 2 tp_dst=9999 controller=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port1 1 1 in_port=1 voip=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port2 1 1 in_port=2 voip=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port3 1 1 in_port=3 data=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port4 1 1 in_port=4 data=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 1 any voip=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 1 any voip=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 1 any data=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any data=7

# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace