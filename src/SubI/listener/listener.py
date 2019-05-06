#  /usr/bin/python3
#  *-* coding: utf-8 *-*

import socket
import struct
import time
import threading
from cmd import Cmd

ADDRESSES = {
    '5009': '127.0.0.0',
    '5010': '127.0.0.0'
}


class Prompt(Cmd):
    intro = 'Type help or ? to list commands.\n'
    prompt = '(listener)\t'
    file = None


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
                print(addr)
            except socket.timeout:
                pass
            except Exception as e:
                sock.close()
                self.alive = False
        print(id_heading_str + 'Switching off')

    def kill(self):
        self.alive = False

def addGateway():
    pass

def main():



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
