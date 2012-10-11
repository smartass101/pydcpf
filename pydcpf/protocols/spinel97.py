from .spinelbase import SpinelBasePacket, ACKError
from random import randint

__all__ = ["RequestPacket", "ResponsePacket"]

class CheckSumError(Exception):
    pass

class Spinel97BasePacket(SpinelBasePacket):
    def calculate_checksum(self):
        end = self.start + self.length - 2
        SUM = 255
        packet = self.raw_packet
        for i in xrange(self.start, end):
            SUM -= packet[i]
        while True: #simulate byte overrun
            if SUM > 0:
                break
            SUM += 256
        return SUM
    
    def check(self):
        if self['ACK'] != '\x00':
            raise ACKError(self['ACK'])
        if self['SUMA'] != self.calculate_checksum():
            raise CheckSumError

Spinel97BasePacket.register_element('NUM', 'Number of bytes in packet after NUM', start_position=2, code='>H')
Spinel97BasePacket.register_element('ADR', 'Module address number', start_position=4, code='>B')
Spinel97BasePacket.register_element('SIG', 'Signature number', start_position=5, code='>B')
Spinel97BasePacket.register_element('DATA', 'Data contained in packet', start_position=7, end_position=-2)
Spinel97BasePacket.register_element('SUMA', 'Checksum number', start_position=-2, code='>B')

class RequestPacket(Spinel97BasePacket):
    """RequestPacket class for the Spinel 97 protocol format"""
    def __init__(self, INST=None, ADR=0xfe, DATA='', NUM=None, SIG=None, SUMA=None, raw_packet=None ):
        if INST is not None or raw_packet is not None:
            super(RequestPacket, self).__init__(raw_packet=raw_packet, PRE='*', FRM=97, ADR=ADR, INST=INST, DATA=DATA, CR='\r')
            if NUM is None:
                NUM = self.length - 4
            self['NUM'] = NUM
            if SIG is None:
                SIG = randint(0, 255)
            self['SIG'] = SIG
            if SUMA is None:
                SUMA = self.calculate_checksum()
            self['SUMA'] = SUMA

RequestPacket.register_element('INST', "Device instruction code character", start_position=6, length=1)

class ResponsePacket(Spinel97BasePacket):
    """ResponsePacket class for the Spinel 97 protocol format"""
    def __init__(self, ACK=None, ADR=0xfe, DATA='', NUM=None, SIG=None, SUMA=None, raw_packet=None ):
        if ACK is not None or raw_packet is not None:
            super(ResponsePacket, self).__init__(raw_packet=raw_packet, PRE='*', FRM=97, ADR=ADR, ACK=ACK, DATA=DATA, CR='\r')
            if NUM is None:
                NUM = self.length - 4
            self['NUM'] = NUM
            if SIG is None:
                SIG = randint(0, 255)
            self['SIG'] = SIG
            if SUMA is None:
                SUMA = self.calculate_checksum()
            self['SUMA'] = SUMA

ResponsePacket.register_element('ACK', 'Acknowledgment code character', start_position=6, length=1)

