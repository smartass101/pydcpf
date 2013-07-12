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


    def get_inputs_measured_value_state(self, address=0xfe):
        """Return the values measured and the state of the 4 channels

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


    def get_inputs_measured_value(self, address=0xfe, *channels):
        """Return the last measured value by the specified channels

        This method checks the status of the reported values

        Parameters
        ----------
        channels: *args, int
            channels to return

        Returns
        -------
        values : list of int
            last measured values by the given channels

        Raises
        ------
        ValueError: if underflow, overflow or invalid value detected or wrong channel reported
        """
        channels_state = self.get_inputs_measured_value_state(address)
        values = []
        for channel in channels:
            channel_nr, (underflow, overflow, valid), value = channels_state[channel - 1]
            if channel_nr == channel and valid and not underflow and not overflow:
                values.append(value)
            elif channel_nr != channel:
                raise ValueError("channel %i reported channel number" % (channel, channel_nr))
            elif underflow:
                raise ValueError("channel %i reported underflow" % channel)
            elif overflow:
                raise ValueError("channel %i reported overflow" % channel)
            elif not valid:
                raise ValueError("channel %i reported invalid value" % channel)
        return values
                             
