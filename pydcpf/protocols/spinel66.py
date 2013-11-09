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



class Spinel66BasePacket(SpinelBasePacket):

    
    def check(self):
        if self.ACK != '0':
            raise ACKError(self)



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
