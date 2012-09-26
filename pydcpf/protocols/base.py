"""This module provides the base :class:`RequestPacket` and :class:`ResponsePacket` classes for documentation purposes."""

class RequestPacket(object):
    """Request packet class

    This class should be used when sending requests to the device
    """

    raw_packet = None
    
    def __init__(self, raw_packet=None, **packet_parameters):
        """Initialize the packet either from the *raw_packet* or from keyword arguments or just simply create it if nothing is specified

        Parameters
        ----------
        raw_packet : bytearray or str or bytes, optional
            If specified, it will be stored as a memoryview in :attr:`RequestPacket.raw_packet`
        **packet_parameters, optional
            keyword parameters used for constructing the packet

        Note
        ----
        This method should NOT be overridden, define your own :meth:`RequestPacket.create` instead!
        """
        if raw_packet is not None:
            self.raw_packet = memoryview(raw_packet)
        elif packet_parameters != {}:
            self.raw_packet = memoryview(self.create(**packet_parameters))

    def create(self, **packet_parameters):
        pass


class ResponsePacket(object):


    raw_packet = None
    
    def extract(self, data_buffer):
        """Try to extract a packet from *data_buffer*

        Parameters
        ----------
        data_buffer : bytearray
            data buffer to extract from

        Returns
        -------
        remnant : bytearray or None
            If successful, store the raw packet as :attr:`ResponsePacket.raw_packet` as a memoryview over the original *data_buffer* and return the remnant from the *data_buffer* 
            If unsuccessful, return None

        Note
        ----
        This method should NOT be overridden, define your own :meth:`ResponsePacket.find_packet` instead!
        """
        start, end = self.find(data_buffer)
        end += 1 # will be using slices, not indexes
        if start is None:
            return None
        else:
            self.raw_packet = memoryview(data_buffer)[start:end]
            return data_buffer[end:]
            
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
        """
        pass

    def check(self, raise_exceptions=True, **parameters):
        """Check and verify the packet, optionally modify the verification method based on keyword *parameters*

        Parameters
        ----------
        **parameters : implementation depednant, optional
            keyword arguments possibly modifying the verification procedure

        Returns
        -------
        error_code : int
            0 if no problems were encountered, non-zero values are implementation depednant and should be described in the docstring
        """
        pass
