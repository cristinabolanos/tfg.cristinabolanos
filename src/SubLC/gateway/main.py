import socket
import struct
import time
import ubinascii
from machine import unique_id
from network import LoRa

lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)

DATA_FORMAT = '!2B' + 'B' + 'BBB'    # Dest | Src | Seq | Tmp | Hum | Soil
DATA_ACK_FORMAT = '!B' + 'B' + ''    # Dest | Seq
SETUP_FORMAT = '!2B' + 'B' + ''      # Dest | Src | Src
SETUP_ACK_FORMAT = '!2B' + 'B' + ''  # Dest | Src | Src

BROADCAST = 255
ID = 10

RECIEVING_WAIT_TIME = 15


def processData(temp, hum, soil):
    print('Recieved {0} {1} {2}'.format(temp, hum, soil))


def recieveData():
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    time0 = time.time()
    print('DEBUG:\tNow recieving data from nodes.')
    while (time.time() - time0 < RECIEVING_WAIT_TIME):
        data = sock.recv(struct.calcsize(DATA_FORMAT))
        if len(data) == struct.calcsize(DATA_FORMAT):
            id, node, data_seq, temp, hum, soil = struct.unpack(
                DATA_FORMAT, data
            )
            processData(temp, hum, soil)
            sock.send(struct.pack(DATA_ACK_FORMAT,
                                  node,
                                  data_seq)
                      )
        elif len(data) == struct.calcsize(SETUP_FORMAT):
            id, node, data_seq = struct.unpack(
                SETUP_FORMAT, data
            )
            sock.send(struct.pack(SETUP_ACK_FORMAT,
                                  node, ID,
                                  data_seq)
                      )


def sendData():
    pass


if __name__ == '__main__':
    while True:
        recieveData()
        sendData()
