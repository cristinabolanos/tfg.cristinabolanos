import time
from machine import enable_irq, disable_irq

class DHT22_johnmcdnz:
    # https://github.com/johnmcdnz/LoPy-DHT-transmission
    def __init__(self, pin):
        self.pin = pin

    def values(self):
        result = self.decode(self.getval(self.pin))
        if result:
            hum = result[0] * 256 + result[1]
            temp = result[2] * 256 + result[3]
            if (temp > 0x7fff):
                temp = 0x8000 - temp
            result = (temp, hum)
        return result

    def getval(self, pin):
        value = []
        time.sleep(1)
        pin(0)
        time.sleep_ms(20) # MODIFIED
        pin(1)
#        time.sleep_us(50) # MODIFIED
        irq = disable_irq()
        for i in range(700): # MODIFIED
            value.append(pin())
        enable_irq(irq)
        return value

    def decode(self, input):
        result = None
        bits = []

        if len(input) != 0:
            print(input)
            result = [0]*5
            one_index = input.index(1, 0)
            zero_index = input.index(0, one_index)

            while len(bits) < len(result)*8:
                try:
                    one_index = input.index(1, zero_index)
                except ValueError:
                    one_index = len(input) - 1
                try:
                    zero_index = input.index(0, one_index)
                except ValueError:
                    zero_index = len(input) - 1
                bits.append(zero_index - one_index)

            for i in range(len(result)):
                for j in bits[i*8:(i+1)*8]:
                    result[i] = result[i] << 1
                    if j > 5:
                        result[i] = result[i]+1

            if (result[0] + result[1] + result[2] +
                result[3])&0xff != result[4]:
                result = None
                print('Checksum error!')
            else:
                result = result[0:4]
        else:
            print('Input empty!')

        return result
