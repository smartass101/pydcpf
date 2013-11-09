#Python device communications protocol framework (pydcpf)
#Copyright (C) 2013  Ondřej Grover
#
#pydcpf is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydcpf is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydcpf.  If not, see <http://www.gnu.org/licenses/>.
from .spinelbase import SpinelBasePacket, ACKError


__all__ = ["RequestPacket", "ResponsePacket"]




class CheckSumError(Exception):

    
    def __init__(self, packet):
        self.packet = packet


    def __str__(self):
        return "Packet checksum is 0x%02x, but the SUMA checksum byte is 0x%02x" % (self.packet.calculate_checksum(), self.packet.SUMA)




class Spinel97BasePacket(SpinelBasePacket):

    
    def calculate_checksum(self):
        end = self.start + self.length - 2
        SUM = 255
        packet = self.raw_packet
        for i in xrange(self.start, end):
            SUM -= packet[i]
        return abs(SUM % 256)

    
    def check(self):
        if self.SUMA != self.calculate_checksum():
            raise CheckSumError(self)
        try:
            if self.ACK != '\x00':
                raise ACKError(self)
        except AttributeError:
            pass # must be a RequestPacket which has INST instead of ACK


    def find(self):
        sup = super(Spinel97BasePacket, self)
        full_buffer_length = len(self.raw_packet)
        if sup.find(): #means we have a candidate at all
            while full_buffer_length - self.start >= 9:
                # first check whether it could be a valid packet
                # based on the count of necessary bytes in packet
                packet_len = self.NUM + 4
                CR_position = self.start + packet_len - 1 #CR_position must be an index
                if CR_position < full_buffer_length and self.raw_packet[CR_position] == 13:
                    # if the last byte is CR as reported by NUM, ord('\r') == 13
                    self.length = packet_len
                    return True
                if not sup.find(self.start + 1): #look for another candidate
                    return False
        else:
            return False
            


Spinel97BasePacket.register_element('NUM', 'Number of bytes in packet after NUM', start_position=2, code='>H')
Spinel97BasePacket.register_element('ADR', 'Module address number', start_position=4, code='>B')
Spinel97BasePacket.register_element('SIG', 'Signature number', start_position=5, code='>B')
Spinel97BasePacket.register_element('DATA', 'Data contained in packet', start_position=7, end_position=-2)
Spinel97BasePacket.register_element('SUMA', 'Checksum number', start_position=-2, code='>B')




class RequestPacket(Spinel97BasePacket):
    """RequestPacket class for the Spinel 97 protocol format"""

    
    def __init__(self, INST=None, ADR=0xfe, DATA='', NUM=None, SIG=None, SUMA=None, raw_packet=None ):
        if raw_packet is not None:
            super(RequestPacket, self).__init__(raw_packet=raw_packet)
        elif INST is not None:
            super(RequestPacket, self).__init__(PRE='*', FRM=97, ADR=ADR, INST=INST, DATA=DATA, CR='\r')
            if NUM is None:
                NUM = self.length - 4
            self.NUM = NUM
            if SIG is None:
                SIG = 2
            self.SIG = SIG
            if SUMA is None:
                SUMA = self.calculate_checksum()
            self.SUMA = SUMA



RequestPacket.register_element('INST', "Device instruction code character", start_position=6, length=1)



class ResponsePacket(Spinel97BasePacket):
    """ResponsePacket class for the Spinel 97 protocol format"""

    
    def __init__(self, ACK=None, ADR=0xfe, DATA='', NUM=None, SIG=None, SUMA=None, raw_packet=None ):
        if ACK is not None or raw_packet is not None:
            super(ResponsePacket, self).__init__(raw_packet=raw_packet, PRE='*', FRM=97, ADR=ADR, ACK=ACK, DATA=DATA, CR='\r')
            if NUM is None:
                NUM = self.length - 4
            self.NUM = NUM
            if SIG is None:
                SIG = 2
            self.SIG = SIG
            if SUMA is None:
                SUMA = self.calculate_checksum()
            self.SUMA = SUMA



ResponsePacket.register_element('ACK', 'Acknowledgment code character', start_position=6, length=1)

