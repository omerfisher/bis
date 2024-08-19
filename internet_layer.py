from ethernet import ETHERNET_HEADER, send_2_layer
from arp import handle_arp


ARP_CODE = 2054


def handle_3_layer(pkt, type_code, my_mac, my_ip, socket):
    """
    Handles a third layer packet.
    :param pkt: The packet in a bytes array format.
    :param type_code: The type of the layer's protocol.
    :param ip: Our ip. 
    """
    pkt = pkt[ETHERNET_HEADER:]
    if type_code == ARP_CODE:
        pkt_to_send, dst_mac = handle_arp(pkt, my_mac, my_ip)
        if pkt_to_send == None:
            return
        send_2_layer(pkt_to_send, dst_mac, my_mac, ARP_CODE, socket)
