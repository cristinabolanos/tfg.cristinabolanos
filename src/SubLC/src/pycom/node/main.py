import socket
import struct
import time
import ubinascii
from machine import unique_id
from network import LoRa

lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)

FIND_GATEWAY_FORMAT = '!6B' + 'B'
FIND_GATEWAY_ACK_FORMAT = '!6B' + '6B' + 'B'
PUSH_FORMAT = '!6B' + 'B'
PUSH_ACK_FORMAT = '!6B' + 'B'

MAC = ubinascii.hexlify(unique_id())
MAC_TUPLE = struct.unpack('!6B', MAC)
GATEWAY_MAC_TUPLE = ()

SEQ_FIND = 0

pkg_seq = 0

def setup():
    print('Setting up...')
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    sock.send(struct.pack(FIND_GATEWAY_FORMAT,
              MAC_TUPLE[0], MAC_TUPLE[1],
              MAC_TUPLE[2], MAC_TUPLE[3],
              MAC_TUPLE[4], MAC_TUPLE[5],
              SEQ_FIND)
              )
    wait_for_ack = True
    while(wait_for_ack):
      ack = sock.recv(6 + 6 + 1)
      if len(ack):
          ack_pkg = struct.unpack(FIND_GATEWAY_ACK_FORMAT, ack)
          ack_mac = ack_pkg[0], ack_pkg[1], ack_pkg[2], ack_pkg[3], ack_pkg[4], ack_pkg[5]
          gateway_mac = ack_pkg[6], ack_pkg[7], ack_pkg[8], ack_pkg[9], ack_pkg[10], ack_pkg[11]
          ack_seq = ack_pkg[12]
          if ack_mac == MAC_TUPLE:
              if ack_seq == pkg_seq:
                  wait_for_ack = False
                  ++pkg_seq
                  GATEWAY_MAC_TUPLE = gateway_mac
                  print('Gateway found on {0}'.format(gateway_mac))
    sock.close()
    time.sleep(5)
    print('Now ready to sending data!')

def get_data():
    pass

def send_data(temp=None, hum=None,
              soil=None):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    sock.send(struct.pack(PUSH_FORMAT,
                          MAC_TUPLE[0], MAC_TUPLE[1],
                          MAC_TUPLE[2], MAC_TUPLE[3],
                          MAC_TUPLE[4], MAC_TUPLE[5],
                          pkg_seq))
    wait_for_ack = True
    while(wait_for_ack):
        ack = sock.recv(6 + 1)
        if len(ack):
            ack_pkg = struct.unpack(PUSH_ACK_FORMAT, ack)
            ack_mac = ack_pkg[0], ack_pkg[1], ack_pkg[2], ack_pkg[3], ack_pkg[4], ack_pkg[5]
            ack_seq = ack_pkg[6]
            if ack_mac == MAC_TUPLE:
                if ack_seq == 1:
                    wait_for_ack = False
                    ++pkg_seq
                    print('Message sended correctly.')
                else:
                    wait_for_ack = False
                    print('Error on message. Try again.')
    sock.close()
    time.sleep(5)

if __name__ == '__main__':
    setup()
    while(True):
        get_data()
        send_data()
