import socket
import struct
import time
import ubinascii
from machine import unique_id
from network import LoRa

lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)

DATA_FORMAT = '!2B' + 'B' + 'BBB'   # Dest | Src | Seq | Tmp | Hum | Soil
DATA_ACK_FORMAT = '!B' + 'B' + ''   # Dest | Seq
SETUP_FORMAT = '!2B' + 'B' + ''     # Dest | Src | Src
SETUP_ACK_FORMAT = '!2B' + 'B' + '' # Dest | Src | Src

BROADCAST = 255
GATEWAY = -1
ID = 1

def getGateway(seq=0):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    sock.send(struct.pack(SETUP_FORMAT,
                          BROADCAST, ID,
                          seq)
              )
    wait_for_ack = True
    while(wait_for_ack):
        ack = sock.recv(struct.calcsize(SETUP_ACK_FORMAT))
        if len(ack):
            id, gateway, ack_seq = struct.unpack(SETUP_ACK_FORMAT, ack)
            if id == ID and ack_seq == seq:
                wait_for_ack = False
    sock.close()
    return gateway

def readSensors():
    pass

def sendData(seq):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    sock.send(struct.pack(DATA_FORMAT,
                          BROADCAST, ID,
                          seq, 0, 0, 0)
              )
    wait_for_ack = True
    while(wait_for_ack):
        ack = sock.recv(struct.calcsize(DATA_ACK_FORMAT))
        if len(ack):
            id, ack_seq = struct.unpack(DATA_ACK_FORMAT, ack)
            if id == ID and ack_seq == seq:
                wait_for_ack = False
                print('Message sended successfully')
    sock.close()

if __name__ == '__main__':
    seq = 0
    GATEWAY = getGateway(seq)
    print('My gateway is {0}'.format(GATEWAY))
    while(True):
        time.sleep(1)
        readSensors()
        sendData(++seq)
