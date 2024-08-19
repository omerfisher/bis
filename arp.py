from ethernet import get_mac_from_bytes, get_ip_from_bytes
from cachetools import TTLCache

OPCODE_START  = 6
OPCODE_STOP = 8
SRC_MAC_START = 8
SRC_MAC_STOP = 14
SRC_IP_START = 14
SRC_IP_STOP = 18
DST_IP_START = 24
DST_IP_STOP = 28
MAC_ADDRESS_TABLE = TTLCache(maxsize=5120, ttl=300)
REQUEST_OPCODE = 1
ETHERNET_TYPE = 1
IPV4_TYPE = 2048
HARDWARE_SIZE = 6
PROTOCOL_SIZE = 4
REPLY_OPCODE = 2


def build_arp_response(src_mac, src_ip, dst_mac, dst_ip):
    pkt = ETHERNET_TYPE.to_bytes(2) + IPV4_TYPE.to_bytes(2) + HARDWARE_SIZE.to_bytes(1) + PROTOCOL_SIZE.to_bytes(1) + REPLY_OPCODE.to_bytes(2)
    pkt += int("".join(src_mac.split(':')), 16).to_bytes(6)
    pkt += b''.join([int(x).to_bytes(1) for x in src_ip.split('.')])
    pkt += int("".join(dst_mac.split(':')), 16).to_bytes(6)
    pkt += b''.join([int(x).to_bytes(1) for x in dst_ip.split('.')])
    return pkt


def handle_arp(pkt, my_mac, my_ip):
    opcode = int.from_bytes(pkt[OPCODE_START:OPCODE_STOP])
    if opcode == REQUEST_OPCODE:
        src_mac = get_mac_from_bytes(pkt, SRC_MAC_START, SRC_MAC_STOP)
        src_ip = get_ip_from_bytes(pkt, SRC_IP_START, SRC_IP_STOP)
        MAC_ADDRESS_TABLE[src_ip] = src_mac
        dst_ip = get_ip_from_bytes(pkt, DST_IP_START, DST_IP_STOP)
        if dst_ip != my_ip:
            return None, None
        return build_arp_response(my_mac, my_ip, src_mac, src_ip), src_mac
