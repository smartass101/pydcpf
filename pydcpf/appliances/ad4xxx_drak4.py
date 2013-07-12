"""This module implements a Device class for communication in Spinel 97 protocol with AD4ETH, AD4RS, AD4USB and Drak 4 devices made by Spinel s.r.o.
"""
import struct

from .. import core

class Device(core.Device):
    """Class representing a AD4ETH, AD4RS, AD4USB and Drak 4
    device made by Spinel s.r.o.

    The Spinel 97 protocol is used for communication
    """

    def __init__(self, address, **kwargs):
        super(Device, self).__init__(address, protocol_module='pydcpf.protocols.spinel97', **kwargs)


    def get_inputs_measured_value(self, address=0xfe):
        """Return the values measured by the 4 channels

        Returns
        -------
        channel_measured_values : list of [int, [bool,bool,bool], int]
            list of 4 lists describing each channel:
                channel_number: int
                [underflow, overflow, valid]: list of bool
                value: int
        """
        data = self.query(INST='\x51',
                          DATA='\x00',  # for future compatibility according to docs
                          ADR=address,
                          )
        channels = []
        for i in xrange(0, 4):          # for all 4 channels
            offset = i*4
            channel_nr, status, value = struct.unpack_from(">cBH", data[offset:offset + 4])
            channels.append([ord(channel_nr),
                             # [ underflow, overflow, valid] ... [3. bit, 4. bit, 8. bit]
                             # in docs bits are indexed form 0, so there it is 2.,3.,7.
                             [bool(status & 8), bool(status & 16), bool(status & 128)],
                             value,
                             ]
                            )
        return channels
    
                             
