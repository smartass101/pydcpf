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
from .. import core


class Device(core.Device):


    def __init__(self, address, **kwargs):
        """Initialize a device communicating with the EVR116 valve

        address is expected to be a socket address of the RS232ETH converter or the
        or path of the serial port character file node

        Serial line settings: 300 Baud, 7 bits, 2 stop bits, log. 0 >7V, log. 1 <3V 
        """
        super(Device, self).__init__(address=address, protocol_module='pydcpf.protocols.evr116', **kwargs)

    def set_position(self, position):
        if position < 512 or position > 6760:
            raise ValueError("position not in range [512, 6760]")
        hex_position = "%x" % (position / 2)
        return self.query(IDENTIFIER='g', DATA=hex_position)


    def get_position(self):
        hex_position = self.query(IDENTIFIER='p', DATA='?')
        return int(str(hex_position), 16)


    def close_valve(self):
        return self.query(IDENTIFIER='x')


    def open_valve(self):
        return self.query(IDENTIFIER='y')

    
