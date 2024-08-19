from scapy.all import conf, IFACES
from ethernet import handle_2_layer
from internet_layer import handle_3_layer


MY_IFACE = 'Intel(R) Wireless-AC 9560 160MHz'
MY_MAC = 'ab:cd:ef:12:34:56'
MY_IP = '10.100.102.200'


def handle_packet(pkt, socket):
    """
    Handles a packet.
    :param pkt: The packet in a bytes array format.
    """
    type_code = handle_2_layer(pkt, MY_MAC)
    if type_code == -1:
        return
    handle_3_layer(pkt, type_code, MY_MAC, MY_IP, socket) 


if __name__ == '__main__':
    socket = conf.L2socket(iface=MY_IFACE, promisc=True)
    
    while True:
        pkt = socket.recv_raw()[1]
        if not pkt:
            continue
        handle_packet(pkt, socket)