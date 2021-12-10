from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,udp,tcp
from ryu.lib.packet import ether_types


class Controller(app_manager.RyuApp):
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
            "00:00:00:00:00:05":3
            }

        }
        self.slice_to_port = {
            2:{2:1,1:2},
            4:{2:1,1:2},
            7:{3:4,4:3}
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
        # self.logger.info("send_msg %s", out)
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.in_port
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        flag = 0
        if pkt.get_protocol(tcp.tcp).dst_port == 21:
            flag = 1
        self.logger.info(f"ADM NOW switch {dpid} in port {in_port}")
        # self.logger.info("packet in s%s in_port=%s eth_src=%s eth_dst=%s pkt=%s udp=%s", dpid, in_port, src, dst, pkt, pkt.get_protocol(udp.udp))
        if (dpid in self.mac_to_port):
            if dpid in self.slice_to_port and in_port in self.slice_to_port[dpid]:
                self.logger.info("ADM sliced")
                out_port = self.slice_to_port[dpid][in_port]
            elif dst in self.mac_to_port[dpid] :

                self.logger.info("ADM Pacchetto arrivato in endswitch")
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            if flag == 0:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src,
                    tp_src=21,
                )
            else:
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    dl_dst=dst,
                    dl_src=src,
                    tp_dst=21,
                )
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
        else:
            out_port = ofproto.OFPP_FLOOD
            self.logger.info("ADM Flooding")
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(
                        in_port=in_port,
                        dl_dst=dst,
                        dl_src=src,
                        tp_dst=5060,
                    )
            self.add_flow(datapath, 1, match, actions)
            
            self._send_package(msg, datapath, in_port, actions)




        


       