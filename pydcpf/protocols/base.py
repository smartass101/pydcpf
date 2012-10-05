"""This module provides the base :class:`RequestPacket` and :class:`ResponsePacket` classes, mainly for documentation purposes (some methods shouldn't to be overridden).
"""

import struct

class RequestPacket(object):
    """Request packet class

    This class should be used when sending requests to the device

    For most protocols this class may be the same as :class:`ResponsePacket`
    """
    packet_length = 0
    
    def __init__(self, raw_packet=None, **packet_parameters):
        """Initialize the packet either from the *raw_packet* or from keyword arguments or just simply create it if nothing is specified

        Parameters
        ----------
        raw_packet : int or bytearray, optional
            If specified, it will be stored in :attr:`RequestPacket.raw_packet`
            If int, an empty bytearray of that size will be made 
        **packet_parameters, optional
            keyword parameters used for constructing the packet
            each keyword argument should be the name of a property defined with :meth:`RequestPacket.make_property`

        Note
        ----
        This method should NOT be overridden, define your own packet structure using :meth:`RequestPacket.make_property` instead!
        """
        if raw_packet is not None:
            if isinstance(raw_packet, int):
                raw_packet = bytearray(raw_packet)
            self.raw_packet = memoryview(raw_packet)
        elif packet_parameters != {}:
            if 'DATA' in packet_parameters:
                self.packet_length += len(packet_parameters['DATA'])
            self.raw_packet = memoryview(bytearray(self.packet_length))
            for name, value in packet_parameters.iteritems():
                setattr(self, name, value)

    @classmethod
    def make_property(cls, name, docstring, start_position=None, code=None, end_position=None, set_function=None, get_function=None):
        """Make a :class:`property` for accessing a part of the packet with Packet.name with a *docstring* which will either unpack or pack a value according to the *format* beginning at *start_position* or set or get a memoryview buffer starting at *start_position* and ending at *end_position* or provide your own *set_function* and *get_function*

        ::
        class RequestPacket(pydcpf.protocols.base.RequestPacket):
        ...
        RequestPacket.make_property('NUM', 'Number of bytes in the packet after NUM', 2, code='>H')
        RequestPacket.make_property('DATA','Data contained in the packet', 6, end_position=-2)

        Parameters
        ----------
        name : str
            name of the property, will be accessible as Packet.name
        docstring : str
            documentation for the property
        start_position : int, optional
            index in the raw_packet buffer at which to start to pack or unpack the value(s)
        code : str, optional
            C type format string, see :module:`struct` for details
            mutually exclusive with *end_position*
        end_position : int, optional
            index in the raw_packet buffer at which the value ends
            mutually exclusive with *code*
            may be negative
        set_function : function
            if not None, it will be used instead of creating one based on *start_position*, *code* or *end_position*
        get_function : function
            if not None, it will be used instead of creating one based on *start_position*, *code* or *end_position*

        Note
        ----
        If you plan on using these properties to set the respective portions of the :attr:`ResponsePacket.raw_buffer`, it is your duty to make sure that the raw_buffer has enough space for the data
        """
        if code is not None:
            self.packet_length += struct.calcsize(code)
        elif end_position > 0:
            self.packet_length += end_position - start_position
        if get_function is None:
            if end_position is None: #want just simple size delimited
                def fget(self):
                    return struct.unpack_from(code, self.raw_packet, start_position)
            else:
                def fget(self):
                    return self.raw_packet[start_position:end_position]
        if set_function is None:
            if end_position is None:
                def fset(self, value):
                    struct.pack_into(code, self.raw_packet, start_position, value)
            else:
                def fset(self, value):
                    self.raw_packet[start_position:end_position] = value
        setattr(self, name, property(fget=fget, fset=fset, doc=docstring))
    


class ResponsePacket(RequestPacket):
    """Response packet class

    This class should be used when receiving responses from the device

    For most protocols this class may be the same as :class:`RequestPacket`
    """

    @staticmethod
    def find(self, data_buffer):
        """Try to find a WHOLE packet in the *data_buffer*
        
        Parameters
        ----------
        data_buffer : bytearray
            data buffer to find the packet in

        Returns
        -------
        start_position : int or None
            index of the starting character of the packet in the *data_buffer*
            if a WHOLE packet cannot be found, return None
        end_position : int
            index of the ending character of the packet in the *data_buffer*

        Note
        ----
        As this method may not need access to the packet object itself, it may be decorated with :func:`staticmethod`
        """
        pass

    def check(self, raise_exceptions=True, **parameters):
        """Check and verify the packet, optionally modify the verification method based on keyword *parameters*

        Parameters
        ----------
        **parameters : implementation dependant, optional
            keyword arguments possibly modifying the verification procedure

        Returns
        -------
        error_code : int
            0 if no problems were encountered, non-zero values are implementation depednant and should be described in the docstring
        """
        pass
