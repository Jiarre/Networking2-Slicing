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

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1 1 1 any controller=7
#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port2 1 1 in_port=2 controller=7
#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port3 1 1 in_port=3 controller=7
#fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1-port4 1 1 in_port=4 controller=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 1 any office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 1 any office1=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 1 any office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any office2=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 6 1 any office3=7

# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace