from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

"""
    Controller Office 3 - "office3"
    - agisce come un normale switch di livello 2
"""
class Office3(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Office3, self).__init__(*args, **kwargs)

        self.mac_to_port = {6:{}}


    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        mod = parser.OFPFlowMod(
            datapath=datapath,
            match=match,
            cookie=0,
            command=ofproto.OFPFC_ADD,
            idle_timeout=20,
            hard_timeout=120,
            priority=priority,
            flags=ofproto.OFPFF_SEND_FLOW_REM,
            actions=actions,
        )
        datapath.send_msg(mod)
        self.logger.info("O3 Flow added")

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)


    # Callback gestione dei pacchetti
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        
        # Variabili
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.in_port
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src
        self.logger.info("INFO packet arrived in s%s (in_port=%s)", dpid, in_port)
        
        # === REGOLE === #
        # Controllo se conosco le porte
        if dpid in self.mac_to_port:
            self.mac_to_port[dpid][src] = in_port
            
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s) w/ mac-to-port rule",
                    dpid,
                    out_port,
                )
                
            else:
                # altrimenti devo fare flooding
                out_port = ofproto.OFPP_FLOOD
            
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

            
            if out_port != ofproto.OFPP_FLOOD:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src
                    
                )
                self.add_flow(datapath, 1, match, actions)
            
            self._send_package(msg, datapath, in_port, actions)



        


       