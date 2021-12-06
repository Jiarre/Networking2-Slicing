import os
import shutil
import sys
import time
import math


from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.term import makeTerm
from mininet.link import TCLink



class Topology(Topo):

    def build(self):
        h1 = self.addHost("h1", ip="192.168.1.11/24")
        h2 = self.addHost("h2", ip="192.168.1.12/24")
        h3 = self.addHost("h3", ip="192.168.1.21/24")
        h4 = self.addHost("h4", ip="192.168.1.22/24")
        h5 = self.addHost("h5", ip="192.168.1.31/24")
        h6 = self.addHost("h6", ip="192.168.1.32/24")
        h7 = self.addHost("h7", ip="192.168.1.41/24")
        h8 = self.addHost("h8", ip="192.168.1.42/24")

        #prova1 = self.addHost("p1",ip="192.168.2.21/24")
        #prova2 = self.addHost("p2",ip="192.168.2.22/24")


        for i in range(5):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        #creo topologia a stella con controller in mezzo
        self.addLink("s1","s2")
        self.addLink("s1","s3")
        self.addLink("s1","s4")
        self.addLink("s1","s5")
        #self.addLink("s2","s3")
        #self.addLink("s4","s5")
        #collego pc agli switch per office1
        self.addLink("s2","h1")
        self.addLink("s2","h2")
        self.addLink("s3","h3")
        self.addLink("s3","h4")
        #collego pc agli switch per office2
        self.addLink("s4","h5")
        self.addLink("s4","h6")
        self.addLink("s5","h7")
        self.addLink("s5","h8")

        #test
        #self.addLink("s1","p1")
        #self.addLink("s1","p2")

def runTopo():
    topo = Topology()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.start()
    for h in net.hosts:
        h.cmd("iperf -s -p 5096 -u &")
    CLI(net)

    # After the user exits the CLI, shutdown the network.
    net.stop()

if __name__ == '__main__':
# This runs if this file is executed directly
    setLogLevel( 'info' )
    runTopo()