import socket
import struct
import time
import ubinascii
import sys
from machine import unique_id
from network import LoRa

lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)

DATA_FORMAT = '!2B' + 'B' + 'BBB'    # Dest | Src | Seq | Tmp | Hum | Soil
DATA_ACK_FORMAT = '!B' + 'B' + ''    # Dest | Seq
SETUP_FORMAT = '!2B' + 'B' + ''      # Dest | Src | Src
SETUP_ACK_FORMAT = '!2B' + 'B' + ''  # Dest | Src | Src

BROADCAST = 255
GATEWAY = -1
ID = 1

SETUP_ACK_TIMEOUT = 2.0
SETUP_ACK_RETRIES = 5
DATA_ACK_TIMEOUT = 2.0
DATA_ACK_RETRIES = 5


def getGateway(seq=0):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.settimeout(SETUP_ACK_TIMEOUT)
    msg = struct.pack(SETUP_FORMAT,
                      BROADCAST, ID,
                      seq)
    wait_for_ack = True
    errors_count = 0
    while wait_for_ack and errors_count < SETUP_ACK_RETRIES:
        sock.send(msg)
        try:
            print('DEBUG:\tWaiting for gateway ID...')
            ack = sock.recv(struct.calcsize(SETUP_ACK_FORMAT))
            if len(ack):
                id, gateway, ack_seq = struct.unpack(SETUP_ACK_FORMAT, ack)
                if id == ID and ack_seq == seq:
                    wait_for_ack = False
        except TimeoutError:
            errors_count += 1
            print('DEBUG:\tMessage timeout. ' +
                  'Error count: {0}'.format(errors_count))
            if errors_count == SETUP_ACK_RETRIES:
                print('ERROR:\tMessage couldn\'t be sended. Switching off.')
                sys.exit(-1)
    sock.close()
    return gateway


def readSensors():
    pass


def sendData(seq):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.settimeout(SETUP_ACK_TIMEOUT)
    msg = struct.pack(DATA_FORMAT,
                      BROADCAST, ID,
                      seq, 0, 0, 0)
    wait_for_ack = True
    errors_count = 0
    print('DEBUG:\tAttempting to send collected data.')
    while wait_for_ack and errors_count < DATA_ACK_RETRIES:
        sock.send(msg)
        try:
            print('DEBUG:\tWaiting for gateway ack...')
            ack = sock.recv(struct.calcsize(DATA_ACK_FORMAT))
            if len(ack):
                id, ack_seq = struct.unpack(DATA_ACK_FORMAT, ack)
                if id == ID and ack_seq == seq:
                    wait_for_ack = False
                    print('Message sended successfully.')
        except TimeoutError:
            errors_count += 1
            print('DEBUG:\tMessage timeout. ' +
                  'Error count: {0}'.format(errors_count))
            if errors_count == DATA_ACK_RETRIES:
                print('ERROR:\tMessage couldn\'t be sended. Switching off.')
                sys.exit(-1)
    sock.close()
    return errors_count >= 10


if __name__ == '__main__':
    seq = 0
    errors = False
    GATEWAY = getGateway(seq)
    print('My gateway is {0}'.format(GATEWAY))
    while not errors:
        time.sleep(5)
        readSensors()
        errors = sendData(++seq)
