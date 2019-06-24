import socket
import struct
import time
import ubinascii
import sys
from machine import unique_id, ADC, Pin
from network import LoRa
from crypto import AES, getrandbits
import sensors
import logging

lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
adc = ADC()

class Sensor:
    class Result:
        def __init__(self, values):
            for attr in values:
                setattr(self, attr, values[attr])

        def __str__(self):
            return '\n'.join((': '.join((attr, str(self.__dict__[attr])))
                             ) for attr in
                            self.__dict__)

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return self.reader.read()


class DHT22_Sensor(Sensor):
    class Reader:
        def __init__(self, pin):
            self.pin = Pin(pin, mode=Pin.OPEN_DRAIN)
            self.pin(1)

        def read(self):
            controller = sensors.DHT22_johnmcdnz(self.pin)
            if controller.values():
                temp, hum = controller.values()
            else:
                temp, hum = (-1, -1)
            return DHT22_Sensor.Result({'temperature': temp,
                                        'humidity': hum}
                                       )

    def __init__(self, pin):
        super(DHT22_Sensor, self).__init__(pin)
        self.reader = self.Reader(self.pin)


class Soil_Sensor(Sensor):
    class Reader:
        def __init__(self, pin):
            self.channel = ADC().channel(pin=pin)

        def read(self):
            return Soil_Sensor.Result({'soil_humidity': self.channel.value()}
                                      )

    def __init__(self, pin):
        super(Soil_Sensor, self).__init__(pin)
        self.reader = self.Reader(self.pin)


DATA_FORMAT = '!' + '2B' + 'B' + 'ffi'    # Dest | Src | Seq | Tmp | Hum | Soil
DATA_ACK_FORMAT = '!' + 'B' + 'B' + ''    # Dest | Seq
SETUP_FORMAT = '!' + '2B' + 'B' + ''      # Dest | Src | Src
SETUP_ACK_FORMAT = '!' + '2B' + 'B' + ''  # Dest | Src | Src

BROADCAST = 255
GATEWAY = -1
ID = 1

KEY = b'+o\x91\x9c\xcbyW\xf3I\xb0\xb0]\xadmJh'
GATEWAY_KEY = b'\xb1T\x14<y\x1e\xc8\xf6\xc2k-\xea\xbc\xd7L*'
IV = None
CIPHER = None

SETUP_ACK_TIMEOUT = 10.0
SETUP_ACK_RETRIES = 5
DATA_ACK_TIMEOUT = 10.0
DATA_ACK_RETRIES = 5

SENSOR_DHT22_PIN = 'P3'
SENSOR_SOIL_PIN = 'P17'
SOIL_SENSOR = Soil_Sensor(SENSOR_SOIL_PIN)
DHT22_SENSOR = DHT22_Sensor(SENSOR_DHT22_PIN)

LOG = logging.Logger(level=logging.DEBUG)


def getGateway(seq=0):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.settimeout(SETUP_ACK_TIMEOUT)
    msg = struct.pack(SETUP_FORMAT,
                      BROADCAST, ID,
                      seq)
    IV = getrandbits(128)
    CIPHER = AES(KEY, AES.MODE_CFB, IV)
    msg = IV + CIPHER.encrypt(msg)
    wait_for_ack = True
    errors_count = 0
    while wait_for_ack and errors_count < SETUP_ACK_RETRIES:
        sock.send(msg)
        try:
            ack = sock.recv(16 + struct.calcsize(SETUP_ACK_FORMAT))
            if len(ack):
                tmp_cipher = AES(GATEWAY_KEY, AES.MODE_CFB, ack[:16])
                ack = tmp_cipher.decrypt(ack[16:])
                id, gateway, ack_seq = struct.unpack(SETUP_ACK_FORMAT, ack)
                if id == ID and ack_seq == seq:
                    wait_for_ack = False
                else:
                    LOG.warning('Recieved message not mine: {} {} {}'.format(
                        id, gateway, ack_seq
                    ))
        except TimeoutError:
            errors_count += 1
            if errors_count == SETUP_ACK_RETRIES:
                LOG.error('Message couldn\'t be sended. Switching off.')
                sock.close()
                sys.exit(-1)
            else:
                time.sleep(5)
        time.sleep(2)
    sock.close()
    LOG.info('My gateway is {0}'.format(gateway))
    return gateway


def readSensors():
    soil_result = SOIL_SENSOR.read()
    dht_result = DHT22_SENSOR.read()
    return (dht_result.temperature,
            dht_result.humidity,
            soil_result.soil_humidity)


def sendData(data, seq):
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.settimeout(SETUP_ACK_TIMEOUT)
    msg = struct.pack(DATA_FORMAT,
                      GATEWAY, ID,
                      seq, data[0], data[1], data[2])
    IV = getrandbits(128)
    CIPHER = AES(KEY, AES.MODE_CFB, IV)
    msg = IV + CIPHER.encrypt(msg)
    wait_for_ack = True
    errors_count = 0
    while wait_for_ack and errors_count < DATA_ACK_RETRIES:
        sock.send(msg)
        LOG.debug(
            'Data sended: {} as temp, {} as hum, {} as soil hum'.format(
                data[0], data[1], data[2]
            )
        )
        try:
            ack = sock.recv(16 + struct.calcsize(DATA_ACK_FORMAT))
            if len(ack):
                tmp_cipher = AES(GATEWAY_KEY, AES.MODE_CFB, ack[:16])
                ack = tmp_cipher.decrypt(ack[16:])
                id, ack_seq = struct.unpack(DATA_ACK_FORMAT, ack)
                if id == ID and ack_seq == seq:
                    wait_for_ack = False
                    LOG.info('Message sended successfully.')
                else:
                    LOG.warning('Recieved message not mine: {} {}'.format(
                        id, ack_seq
                    ))
        except TimeoutError:
            errors_count += 1
            if errors_count == DATA_ACK_RETRIES:
                LOG.error('Message couldn\'t be sended. Switching off.')
                sock.close()
                sys.exit(-1)
            else:
                time.sleep(5)
        time.sleep(2)
    sock.close()


if __name__ == '__main__':
    seq = 0
    GATEWAY = getGateway(seq)
    while True:
        time.sleep(25)
        data = readSensors()
        sendData(data, ++seq)
