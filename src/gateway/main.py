import socket
import struct
import time
import ubinascii
from machine import unique_id
from network import LoRa, WLAN
from crypto import AES, getrandbits
import logging

lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
wlan = WLAN(mode=WLAN.STA)

DATA_FORMAT = '!' + '2B' + 'B' + 'ffi'    # Dest | Src | Seq | Tmp | Hum | Soil
DATA_ACK_FORMAT = '!' + 'B' + 'B' + ''    # Dest | Seq
SETUP_FORMAT = '!' + '2B' + 'B' + ''      # Dest | Src | Src
SETUP_ACK_FORMAT = '!' + '2B' + 'B' + ''  # Dest | Src | Src
AREA_DATA_FORMAT = '!B' + 'ffi'           # Gateway ID | Tmp | Hum | Soil

BROADCAST = 255
ID = 10

KEY = b'\xb1T\x14<y\x1e\xc8\xf6\xc2k-\xea\xbc\xd7L*'
NODE_KEY = b'+o\x91\x9c\xcbyW\xf3I\xb0\xb0]\xadmJh'
IV = None
CIPHER = None

RECIEVING_WAIT_TIME = 15

AWS_ADDR = ('ec2-54-80-153-215.compute-1.amazonaws.com', 5009)

LOG = logging.Logger(level=logging.DEBUG)


def wlan_setup(ssid='LoPyAP',
               auth=(WLAN.WPA2, 'contrasenuev1')
               ):
    wlan.connect(ssid=ssid, auth=auth)
    while not wlan.isconnected():
        time.sleep_ms(50)
    LOG.info('My IP is {}'.format(wlan.ifconfig()[0]))


def recieveData():
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    time0 = time.time()
    while (time.time() - time0 < RECIEVING_WAIT_TIME):
        data = sock.recv(16 + struct.calcsize(DATA_FORMAT))
        if data:
            tmp_cipher = AES(NODE_KEY, AES.MODE_CFB, data[:16])
            data = tmp_cipher.decrypt(data[16:])
            if len(data) == struct.calcsize(DATA_FORMAT):
                id, node, data_seq, temp, hum, soil = struct.unpack(
                    DATA_FORMAT, data
                )
                if id == ID:
                    sendData(temp, hum, soil)
                    msg = struct.pack(DATA_ACK_FORMAT,
                                      node,
                                      data_seq)
                    IV = getrandbits(128)
                    CIPHER = AES(KEY, AES.MODE_CFB, IV)
                    msg = IV + CIPHER.encrypt(msg)
                    sock.send(msg)
                else:
                    LOG.warning(
                        'Message not mine: {} {} {} {} {}'.format(
                            id, node, data_seq, temp, hum, soil
                        )
                    )
            elif len(data) == struct.calcsize(SETUP_FORMAT):
                id, node, data_seq = struct.unpack(
                    SETUP_FORMAT, data
                )
                msg = struct.pack(SETUP_ACK_FORMAT,
                                  node, ID,
                                  data_seq)
                IV = getrandbits(128)
                CIPHER = AES(KEY, AES.MODE_CFB, IV)
                msg = IV + CIPHER.encrypt(msg)
                sock.send(msg)
        time.sleep_ms(50)


def sendData(temp, hum, soil):
    LOG.debug(
        'Data recieved: {} as temp, {} as hum, {} as soil hum'.format(
            temp, hum, soil
        )
    )
    msg = struct.pack(AREA_DATA_FORMAT,
                      ID, temp, hum, soil)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(AWS_ADDR)
    sock.send(msg)
    sock.close()


if __name__ == '__main__':
    wlan_setup()
    LOG.info('Now recieving data from nodes.')
    while True:
        recieveData()
