import socket
import struct
import ubinascii
from machine import unique_id
from network import LoRa

lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
sock.setblocking(False)

FOUND_NODE_FORMAT = '!6B' + 'B'
FOUND_NODE_ACK_FORMAT = '!6B' + '6B' + 'B'
PULL_FORMAT = '!6B' + 'B'
PULL_ACK_FORMAT = '!6B' + 'B'

MAC = ubinascii.hexlify(unique_id())
MAC_TUPLE = struct.unpack('!6B', MAC)

print('Ready to recieve data from sensors...')
while(True):
    req = sock.recv(6 + 1)
    if len(req):
        req_pkg = struct.unpack(PULL_FORMAT, req)
        req_mac = req_pkg[0], req_pkg[1], req_pkg[2], req_pkg[3], req_pkg[4], req_pkg[5]
        req_seq = req_pkg[6]
        print('Answering {0}...'.format(
            req_mac
        ))
        if req_seq == 0:
            print(struct.unpack(FOUND_NODE_ACK_FORMAT,
                struct.pack(FOUND_NODE_ACK_FORMAT,
                                      req_pkg[0], req_pkg[1],
                                      req_pkg[2], req_pkg[3],
                                      req_pkg[4], req_pkg[5],
                                      MAC_TUPLE[0], MAC_TUPLE[1],
                                      MAC_TUPLE[2], MAC_TUPLE[3],
                                      MAC_TUPLE[4], MAC_TUPLE[5],
                                      req_seq)))
            sock.send(struct.pack(FOUND_NODE_ACK_FORMAT,
                                  req_pkg[0], req_pkg[1],
                                  req_pkg[2], req_pkg[3],
                                  req_pkg[4], req_pkg[5],
                                  MAC_TUPLE[0], MAC_TUPLE[1],
                                  MAC_TUPLE[2], MAC_TUPLE[3],
                                  MAC_TUPLE[4], MAC_TUPLE[5],
                                  req_seq)
                                  )
        else:
            sock.send(struct.pack(PULL_ACK_FORMAT,
                                  req_pkg[0], req_pkg[1],
                                  req_pkg[2], req_pkg[3],
                                  req_pkg[4], req_pkg[5],
                                  req_seq)
                                  )
