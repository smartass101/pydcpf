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

valid_command_characters = "hxyzijgstv" # request chars
valid_command_characters += "p" + valid_command_characters.upper() # response chars


class RequestPacket(base.RequestPacket):


    def __init__(self, IDENTIFIER='x', DATA=''):
        super(RequestPacket, self).__init__(IDENTIFIER=IDENTIFIER, DATA=DATA, TERMINATOR='\r\n')

    def check(self):
        pass

    def find(self, buffer_start=0):
        raw_packet = self.raw_packet
        try:
            end = raw_packet.index('\r\n', buffer_start) + 1
        except ValueError:
            return False
        possible_start = raw_packet.rfind('\r\n', buffer_start, end - 1)
        if possible_start == -1:
            possible_start = buffer_start
        else:
            possible_start += 2
        possible_packet_buff = buffer(raw_packet, possible_start, end - possible_start - 1)
        for char in reversed(possible_packet_buff):
            if char in valid_command_characters:
                self.start = raw_packet.rfind(char, possible_start, end - 2)
                self.length = end - self.start + 1
                return True
        # might be a reposnse to 'p?' query - only 4 bytes with no identifier
        if len(possible_packet_buff) == 4:
            self.start = possible_start
            self.length = end - possible_start + 1
            return True
        return False



RequestPacket.register_element("IDENTIFIER", "initializing character identifying command", start_position=0, length=1)
RequestPacket.register_element("DATA", "data contained in packet", start_position=1, end_position=-2)
RequestPacket.register_element("TERMINATOR", "terminating characters", start_position=-2, length=2)

ResponsePacket = RequestPacket
