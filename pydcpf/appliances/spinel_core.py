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

