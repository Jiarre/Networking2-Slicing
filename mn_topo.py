import os
import shutil
import sys
import time
import math


from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSKernelSwitch, RemoteController, Node
from mininet.term import makeTerm
from mininet.link import TCLink
from comnetsemu.net import Containernet


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class Topology(Topo):

    def build(self):
        
        h11 = self.addHost("it1", ip="192.168.2.73/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:0c')
        h12 = self.addHost("it2", ip="192.168.2.74/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:0d')

        h1 = self.addHost("a3", ip="192.168.2.21/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:01')
        h2 = self.addHost("a4", ip="192.168.2.41/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:02')
        h3 = self.addHost("h1", ip="192.168.2.22/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:03')
        h4 = self.addHost("h2", ip="192.168.2.31/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:04')
        h5 = self.addHost("h3", ip="192.168.2.32/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:05')
        h6 = self.addHost("h4", ip="192.168.2.42/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:06')
        h7 = self.addHost("h5", ip="192.168.2.51/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:07')
        h8 = self.addHost("h6", ip="192.168.2.52/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:08')

        h9 = self.addHost("a1", ip="192.168.3.61/24",defaultRoute='via 192.168.3.1',mac='00:00:00:00:00:09')
        h10 = self.addHost("a2", ip="192.168.3.62/24",defaultRoute='via 192.168.3.1',mac='00:00:00:00:00:0a')

        

        h13 = self.addHost("sftp", ip="192.168.2.75/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:0b')

        r1 = self.addHost("r1",cls=LinuxRouter,ip="192.168.2.1/24",mac='00:00:00:00:00:0e')
        r2 = self.addHost("r2",cls=LinuxRouter,ip="192.168.3.1/24",mac='00:00:00:00:00:0f')
        
        
        #prova1 = self.addHost("p1",ip="192.168.2.22/24")
        #prova2 = self.addHost("p2",ip="192.168.2.22/24")


        for i in range(7):
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
        self.addLink("s2","a3")
        self.addLink("s2","h1")
        self.addLink("s3","h2")
        self.addLink("s3","h3")
        #collego pc agli switch per office2
        self.addLink("s4","a4")
        self.addLink("s4","h4")
        self.addLink("s5","h5")
        self.addLink("s5","h6")

        self.addLink("s6","a1")
        self.addLink("s6","a2")

        self.addLink("s7","it1")
        self.addLink("s7","it2")
        self.addLink("s7","sftp")
        
        
        self.addLink("s1","r1",intfName2='r1-eth1',params2={'ip':'192.168.2.1/24'})
        self.addLink("s6","r2",intfName2='r2-eth1',params2={'ip':'192.168.3.1/24'})
        self.addLink("s1","s7")

        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
              
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
    n = net.getNodeByName("s7")
    print("*** Setting up bridge network")
    time.sleep(0.1)
    n.cmd('sudo ovs-vsctl add-port s7 eth1')
    net['r1'].cmd("sudo ip route add 192.168.3.0/24 via 10.100.0.2 dev r1-eth2")
    net['r2'].cmd("sudo ip route add 192.168.2.0/24 via 10.100.0.1 dev r2-eth2")

    
    net['sftp'].cmd("python3 sshsocket.py &")
    time.sleep(0.3)
    voip = [net['h1'],net['h2'],net['h3'],net['h4'],net['h5'],net['h6'],net['a1'],net['a2'],net['a3'],net['a4'],net['it1'],net['it2']]
    for h in voip:
        h.cmd("python3 voipsocket.py &")
        time.sleep(0.1)
        print(f"Started {str(h)} socket")



    print("All socket started")
    n.cmd("hostname comnetsemu")
    
    CLI(net)

    # After the user exits the CLI, shutdown the network.
    net.stop()

if __name__ == '__main__':
# This runs if this file is executed directly
    setLogLevel( 'info' )
    runTopo()