#  /usr/bin/python3
#  *-* coding: utf-8 *-*

import socket
import struct
import time
import threading
import datetime
from peewee import MySQLDatabase, Model, FloatField, IntegerField, DateTimeField
from Crypto.Cipher import AES

ADDRESSES = {
    '5009': ''
}

DB = MySQLDatabase('example',
                   user='listener',
                   password='secret',
                   host='local_mysql',
                   port=3306
                   )

AREA_DATA_FORMAT = '!3B' #   | Tmp | Hum | Soil

KEY_GATEWAY_010 = b'.?Gateway-_ 010#'


class Environment(Model):
    area = IntegerField()
    temperature = FloatField()
    humidity = FloatField()
    moisture = FloatField()
    dat = DateTimeField()

    class Meta:
        database = DB
        db_table = 'env'


class Listener(threading.Thread):
    def __init__(self, host, port):
        super(Listener, self).__init__()
        self.host = host
        self.port = port
        self.alive = True

    def run(self):
        myself = threading.current_thread()
        id_heading_str = 'THREAD {0}:\t'.format(myself.name)
        print(id_heading_str + 'Up')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        sock.bind((self.host, int(self.port)))
        while self.alive:
            try:
                sock.listen()
                conn, addr = sock.accept()
                msg = conn.recv(struct.calcsize(AREA_DATA_FORMAT))
                temp, hum, soil = struct.unpack(AREA_DATA_FORMAT, msg)
                Environment(area=2,
                            dat=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            temperature=temp,
                            moisture=hum,
                            humidity=soil
                            ).save()
            except socket.timeout:
                pass
            except Exception as e:
                print(e)
                sock.close()
                self.alive = False
        print(id_heading_str + 'Switching off')

    def kill(self):
        self.alive = False

if __name__ == '__main__':
    try:
        for key in ADDRESSES:
            thread = Listener(host=ADDRESSES[key],
                              port=key)
            thread.setName(key)
            thread.start()
        for thread in threading.enumerate():
            if thread.ident != threading.get_ident():
                thread.join()
    except KeyboardInterrupt:
        print('\nFATHER:\tEnding childs life')
    except Exception as e:
        print(e)
    finally:
        for thread in threading.enumerate():
            if thread.ident != threading.get_ident():
                thread.kill()
