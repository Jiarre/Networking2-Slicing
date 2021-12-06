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
        pc1 = self.addHost("pc1", ip="192.168.1.11/24")
        voip1 = self.addHost("v1", ip="192.168.1.12/24")
        pc2 = self.addHost("pc2", ip="192.168.1.21/24")
        voip2 = self.addHost("v2", ip="192.168.1.22/24")
        pc3 = self.addHost("pc3", ip="192.168.1.31/24")
        voip3 = self.addHost("v3", ip="192.168.1.32/24")
        pc4 = self.addHost("pc4", ip="192.168.1.41/24")
        voip4 = self.addHost("v4", ip="192.168.1.42/24")


        for i in range(5):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        #creo topologia a stella con controller in mezzo
        self.addLink("s1","s2")
        self.addLink("s1","s3")
        self.addLink("s1","s4")
        self.addLink("s1","s5")
        #collego voip agli switch per i voip
        self.addLink("s2","v1")
        self.addLink("s2","v2")
        self.addLink("s3","v3")
        self.addLink("s3","v4")
        #collego pc agli switch dati
        self.addLink("s4","pc1")
        self.addLink("s4","pc2")
        self.addLink("s5","pc3")
        self.addLink("s5","pc4")

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

    CLI(net)

    # After the user exits the CLI, shutdown the network.
    net.stop()

if __name__ == '__main__':
# This runs if this file is executed directly
    setLogLevel( 'info' )
    runTopo()