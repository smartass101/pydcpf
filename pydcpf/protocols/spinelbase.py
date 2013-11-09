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
from .base import ResponsePacket



class ACKError(Exception):
    """Acknowledgment code error

    Attributes
    ----------
    ACK : str
        Acknowledgment code in the packet
    """

    descriptions = {
            0x00 : "OK",
            0x01 : "Unknown error",
            0x02 : "Invalid instruction",
            0x03 : "Invalid instruction parameters",
            0x04 : "Permission denied", #write error, too low data, channel disabled, other requirements not met
            0x05 : "Device malfunction",
            0x06 : "Data not available",
            0x0d : "Digital input state change", #automatically sent message
            0x0e : "Continuous measurement", #automatically sent, repeatedly sending measured data
            0x0f : "Range overrun" #automatically sent
        }

    
    def __init__(self, packet):
        self.packet = packet

        
    def __str__(self):
        try:
            int_ACK = int(self.packet.ACK, 16)
        except ValueError: #must be something like '\x0d', so use ord
            int_ACK = ord(self.packet.ACK)
        try:
            return "Non-zero acknowledgment code 0x%02x: " %  int_ACK + self.__class__.descriptions[int_ACK]
        except KeyError: #unknow error code
            return "Unknown acknowledgment code 0x%02x" % int_ACK


    
class SpinelBasePacket(ResponsePacket):


    def find(self, buffer_start=0):
        raw_packet = self.raw_packet #minimize attr lookups
        try:
            start = raw_packet.index('*', buffer_start)
            end = raw_packet.index('\r', start)
        except ValueError:
            return False
        self.start, self.length = start, end - start + 1
        return True



SpinelBasePacket.register_element('PRE', "Packet prefix character", start_position=0, length=1)
SpinelBasePacket.register_element('FRM', "Packet format number", start_position=1, code='>B')
SpinelBasePacket.register_element('CR', "Ending mark character", start_position=-1, length=1)
