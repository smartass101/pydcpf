from .spinelbase import SpinelBasePacket, ACKError

__all__ = ["RequestPacket", "ResponsePacket"]

class Spinel66BasePacket(SpinelBasePacket):
    def check(self):
        if self['ACK'] != '0':
            raise ACKError(self['ACK'])

Spinel66BasePacket.register_element('ADR', "Module address character", start_position=2, length=1)
Spinel66BasePacket.register_element('DATA', "Data contained in packet", start_position=4, end_position=-1)

class RequestPacket(Spinel66BasePacket):
    """RequestPacket class for the Spinel 66 protocol format"""
    def __init__(self, INST=None, ADR='$', DATA='', raw_packet=None ):
        if INST is not None or raw_packet is not None:
            super(RequestPacket, self).__init__(raw_packet=raw_packet, PRE='*', FRM=66, ADR=ADR, INST=INST, DATA=DATA, CR='\r')

RequestPacket.register_element('INST', "Device instruction code character", start_position=3, length=1)

class ResponsePacket(Spinel66BasePacket):
    """ResponsePacket class for the Spinel 66 protocol format"""
    def __init__(self, ACK=None, ADR='$', DATA='', raw_packet=None ):
        if ACK is not None or raw_packet is not None:
            super(ResponsePacket, self).__init__(raw_packet=raw_packet, PRE='*', FRM=66, ADR=ADR, ACK=ACK, DATA=DATA, CR='\r')

ResponsePacket.register_element('ACK', 'Acknowledgment code character', start_position=3, end_position=4)
