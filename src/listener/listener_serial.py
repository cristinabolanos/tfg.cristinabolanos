#  /usr/bin/python3
#  *-* coding: utf-8 *-*

#   Dependencies: pyserial

import sys
import struct
import serial

DATA_FORMAT = '!2B' + 'BBB'   #   Id.Terreno | Id.Area | Datos x3

GATEWAY_PORT = '/dev/ttyUSB0'

if __name__ == '__main__':
    try:
        listener = serial.Serial(port=GATEWAY_PORT,
                                baudrate=115200
                                )
        listener.open()
        while True:
            data = listener.read(stuct.calcsize(DATA_FORMAT))
            print(data)
    except serial.SerialException as e:
        print('Nada en {0}. Saliendo.'.format(GATEWAY_PORT))
        print(e)
        sys.exit(-1)
    except KeyboardInterrupt:
        listener.close()
        sys.exit(0)
