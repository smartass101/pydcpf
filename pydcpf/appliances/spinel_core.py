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
"""This module defines a customized Device class specific to the Spinel protocol

the main difference is that the device will not expect a response when querying a broadcast or universal address
"""

from .. import core


class Device(core.Device):


    def query(self, send_byte_count=None, receive_byte_count=None, check_parameters=dict(), **packet_parameters):
        """Query the device and expect a response based on the address

        According to the Spinel protocol specification,
        if address is the special broadcast or universal address,
        the device will not send a response
        """
        if packet_parameters['ADR'] in [0xff, 0xfe, '%', '$']:
            self.send_request(send_byte_count, **packet_parameters)
        else:
            return super(Device, self).query(send_byte_count, receive_byte_count, check_parameters, **packet_parameters)

