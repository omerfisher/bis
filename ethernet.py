DST_MAC_START = 0
DST_MAC_STOP = 6
SRC_MAC_START = 6
SRC_MAC_STOP = 12
BROADCAST = 'ff:ff:ff:ff:ff:ff'
TYPE_START = 12
TYPE_STOP = 14


def get_addr_from_bytes(pkt, start, stop):
    """
    Returns a mac address from a packet.
    :param pkt: The packet in a bytes array format.
    :param start: The index the address starts at.
    :param stop: The index the address stops at.
    :return: The mac address.
    """
    addr = ''
    for i in range(start, stop):
        tmp = hex(pkt[i])[2:]
        if len(tmp) == 1:
            tmp = '0' + tmp
        addr += tmp + ":"
    return addr[:-1]


def get_dst_mac(pkt):
    """
    Returns a destinaition mac address from a packet.
    :param pkt: The packet in a bytes array format.
    :return: The destination mac address.
    """
    return get_addr_from_bytes(pkt, DST_MAC_START, DST_MAC_STOP)


def get_src_mac(pkt):
    """
    Returns a source mac address from a packet.
    :param pkt: The packet in a bytes array format.
    :return: The source mac address.
    """
    return get_addr_from_bytes(pkt, SRC_MAC_START, SRC_MAC_STOP)


def handle_2_layer(pkt, my_mac):
    """
    Handles a second layer packet.
    :param pkt: The packet in a bytes array format.
    :param my_mac: The mac address of my interface.
    :return: The type of the next layer's protocol, -1 if the packet is not destined to us.
    """
    dst_mac = get_dst_mac(pkt)
    if dst_mac != my_mac and dst_mac != BROADCAST:
        return -1
    return int.from_bytes(pkt[TYPE_START:TYPE_STOP])