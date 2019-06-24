CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0


class Logger():
    def __init__(self, level=NOTSET,
                 format='{level}:\t{msg}'):
        self.level = level
        self.format = format

    def debug(self, msg):
        if self.level <= DEBUG:
            print(self.format.format(
                level='DEBUG',
                msg=msg
            ))

    def info(self, msg):
        if self.level <= INFO:
            print(self.format.format(
                level='INFO',
                msg=msg
            ))

    def error(self, msg):
        if self.level <= ERROR:
            print(self.format.format(
                level='ERROR',
                msg=msg
            ))

    def warning(self, msg):
        if self.level <= WARNING:
            print(self.format.format(
                level='WARNING',
                msg=msg
            ))

    def critical(self, msg):
        if self.level <= CRITICAL:
            print(self.format.format(
                level='CRITICAL',
                msg=msg
            ))
