from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,udp,tcp,ipv4
from ryu.lib.packet import ether_types

"""
    Controller amministrazione - "Administration"
    - permette la connessione a sftp
    - permette il ping tra host
"""
class Administration(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        # out_port = slice_to_port[dpid][in_port]
        #self.mac_to_port = {4:{},5:{}}
        self.mac_to_port = {
            6:{
            "00:00:00:00:00:01":1,
            "00:00:00:00:00:02":2
            },
            2:{
            "00:00:00:00:00:03":2
            },
            4:{
            "00:00:00:00:00:04":2
            },
            7:{
            "00:00:00:00:00:05":3,
            "dc:a6:32:92:27:62":5
            }

        }

        # se arriva mshh su porta 2 lo esco su
        self.slice_to_port = {
            2:{2:1,1:2},
            4:{2:1,1:2}
        }
        
        self.end_switches = [2,4,7,6]


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
        self.logger.info("Administration Flow added")
        datapath.send_msg(mod)


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
        ipv = pkt.get_protocol(ipv4.ipv4)
        tcpp = pkt.get_protocol(tcp.tcp)
        
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src
        flag = 0
        if tcpp.dst_port == 22:
            flag = 1
    
        self.logger.info(f"ADM NOW switch {dpid} in port {in_port}")
        
        # === REGOLE === #
        if (dpid in self.mac_to_port):
            # 
            if dpid in self.slice_to_port and in_port in self.slice_to_port[dpid]:
                self.logger.info("ADM sliced")
                out_port = self.slice_to_port[dpid][in_port]
            # 
            elif dst in self.mac_to_port[dpid] :
                self.logger.info("ADM Pacchetto arrivato in endswitch")
                out_port = self.mac_to_port[dpid][dst]
            else:
                # altrimenti devo fare flood               
                out_port = ofproto.OFPP_FLOOD
                
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

            # se e' destinazione        
            if flag == 1:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src,
                    tp_dst = 22
                    )
            else:
                # se invece è src
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src,
                    tp_src = 22
                    )

            # se non devo fare flooding, allora ???
            if out_port!=ofproto.OFPP_FLOOD:
                self.add_flow(datapath, 2, match, actions)
            self._send_package(msg, datapath, in_port, actions)

        # ...
        else:
            out_port = ofproto.OFPP_FLOOD
            self.logger.info("ADM Flooding")
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]      
            self._send_package(msg, datapath, in_port, actions)
            




        


       