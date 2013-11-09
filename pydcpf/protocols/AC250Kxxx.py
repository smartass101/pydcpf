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
from . import base


def _hexify(value):
    """trasform a number into a 1 Byte hex representation suitable for communication"""
    return "%02X" % value


def _dehexify(hexbytestring):
    """Transform a 2-char bytestring representing a number"""
    return int(str(hexbytestring), 16)


class _basePacket(base.RequestPacket):


    def _set_address(self, address):
        self.raw_packet[1:3] = _hexify(address)

    def _get_address(self):
        return _dehexify(self.raw_packet[1:3])


_basePacket.register_element("INIT", "initializing character", start_position=0, length=1)
_basePacket.register_element("ADR", "device address in decimal", set_function=_basePacket._set_address, get_function=_basePacket._get_address, length=2)
_basePacket.register_element("CR", "terminating character", start_position=-1, length=1)

    

class RequestPacket(_basePacket):


    def __init__(self, ADR=10, DATA=''):
        super(RequestPacket, self).__init__(INIT='@', ADR=ADR, DATA=DATA, CR='\r')
        _sum = 0
        for i in self.raw_packet[1:-3]:
            _sum += i
        while _sum > 256: #the sum must be lesser or equal to 256
            _sum -= 256
        self.CTRLSUM = _sum


    def _set_ctrlsum(self, value):
        self.raw_packet[-3:-1] = _hexify(value)


    def _get_ctrlsum(self):
        return _dehexify(self.raw_packet[-3:-1])


    def find(self):
        pass


RequestPacket.register_element("DATA", "data contained in packet", start_position=3, end_position=-3)
RequestPacket.register_element("CTRLSUM", "control sum in decimal", set_function=RequestPacket._set_ctrlsum, get_function=RequestPacket._get_ctrlsum, length=2)



class ResponsePacket(_basePacket):


    def find(self):
        raw_packet = self.raw_packet #minimize attr lookups
        try:
            start = raw_packet.index('#')
            end = raw_packet.index('\r', start)
        except ValueError:
            return False
        self.start, self.length = start, end - start + 1
        return True


import copy
#to prevent conflicts with previous DATA definition
ResponsePacket.elements_definitions_dict = copy.copy(ResponsePacket.elements_definitions_dict)
ResponsePacket.register_element("DATA", "data contained in packet", start_position=3, end_position=-1)
