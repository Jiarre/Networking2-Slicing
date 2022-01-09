from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,udp,tcp
from ryu.lib.packet import ether_types

"""
    Controller principale - "Controller"
    - pacchetti VOIP possono uscire dallo slice
    - altri pacchetti vengono rimessi all'interno dello slice 
"""
class Controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        self.mac_to_port = {1:{}}
        self.slice_to_port = {
            1: {3:4,4:3,1:2,2:1,5:5,6:6}
        }
        self.administration_mac = ["00:00:00:00:00:01","00:00:00:00:00:02","00:00:00:00:00:0e","00:00:00:00:00:0b","dc:a6:32:92:27:62","00:00:00:00:00:0c","00:00:00:00:00:0d"]
        
    


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
        self.logger.info("CONTROLLER Flow added")


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
        self.logger.info("CONTROLLER packet arrived in s%s (in_port=%s) dal src: %s dst: %s", dpid, in_port,src,dst)
        self.mac_to_port[dpid][src] = in_port
        # === REGOLE === #
        # Pacchetto VOIP
        if pkt.get_protocol(udp.udp) and ((pkt.get_protocol(udp.udp).dst_port == 5060)or(pkt.get_protocol(udp.udp).src_port == 5060)):
                self.logger.info("CONTROLLER Pacchetto VOIP")
                 
                # sorgente o destinazione?
                flag = 0
                if pkt.get_protocol(udp.udp).dst_port == 5060:
                    flag = 1

                # se la destinazione è conosciuta
                if dst in self.mac_to_port[dpid]:
                    # salvo la porta di output
                    out_port = self.mac_to_port[dpid][dst]
                else:
                    # altrimenti devo fare flooding
                    out_port = ofproto.OFPP_FLOOD
                    
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                
                # setto i parametri se pacchetto in uscita o entrata
                if flag == 1:
                    match = datapath.ofproto_parser.OFPMatch(
                        in_port=in_port,
                        tp_dst = 5060,      # qui setto dst
                        dl_dst=dst,
                        dl_src=src  
                    )
                else:
                    match = datapath.ofproto_parser.OFPMatch(
                        in_port=in_port,
                        tp_src = 5060,      # qui setto src
                        dl_dst=dst,
                        dl_src=src
                    )

                if out_port != ofproto.OFPP_FLOOD:
                    self.add_flow(datapath, 3, match, actions)
                self._send_package(msg, datapath, in_port, actions)
        if pkt.get_protocol(tcp.tcp) and ((pkt.get_protocol(tcp.tcp).dst_port == 22)or(pkt.get_protocol(tcp.tcp).src_port == 22)) and (src in self.administration_mac and dst in self.administration_mac):
            self.logger.info("CONTROLLER Pacchetto SFTP Administration")
            
            # sorgente o destinazione?
            flag = 0
            if pkt.get_protocol(tcp.tcp).dst_port == 22:
                flag = 1

            # se la destinazione è conosciuta
            if dst in self.mac_to_port[dpid]:
                # salvo la porta di output
                out_port = self.mac_to_port[dpid][dst]
            else:
                # altrimenti devo fare flooding
                out_port = ofproto.OFPP_FLOOD
                
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            
            # setto i parametri se pacchetto in uscita o entrata
            if flag == 1:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    tp_dst = 22,      # qui setto dst
                    dl_dst=dst,
                    dl_src=src  
                )
            else:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    tp_src = 22,      # qui setto src
                    dl_dst=dst,
                    dl_src=src
                )

            if out_port != ofproto.OFPP_FLOOD:
                self.add_flow(datapath, 3, match, actions)
            self._send_package(msg, datapath, in_port, actions)
        # Pacchetto non VOIP, lo rimetto nel suo slice a seconda di slice_to_port
        elif dpid in self.mac_to_port:
            self.mac_to_port[dpid][src] = in_port
            
            out_port = self.slice_to_port[dpid][in_port]
            if out_port != 0:
                self.logger.info("CONTROLLER invio pacchetto GENERICO")
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self._send_package(msg, datapath, in_port, actions)



        


       