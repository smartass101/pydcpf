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
"""This module provides the base :class:`RequestPacket` and :class:`ResponsePacket` classes, mainly for documentation purposes (some methods shouldn't to be overridden).
"""

__all__ = ["RequestPacket", "ResponsePacket"]

import struct



class RequestPacket(object):
    """Request packet class

    This class should be used when sending requests to the device

    For most protocols this class may be the same as :class:`ResponsePacket`
    """
    
    
    def __init__(self, raw_packet=None, **packet_parameters):
        """Initialize the packet either from the *raw_packet* or from keyword arguments or just simply create it if nothing is specified

        Parameters
        ----------
        raw_packet : int or bytearray, optional
            If specified, it will be stored in :attr:`RequestPacket.raw_packet`
            If int, an empty bytearray of that size will be made 
        **packet_parameters, optional
            keyword parameters used for constructing the packet
            each keyword argument should be the name of a property defined with :meth:`RequestPacket.register_element`

        Note
        ----
        This method should NOT be completely overridden, define your own packet structure using :meth:`RequestPacket.register_element` instead or remember to call it at the end of your own __init__!
        """
        if raw_packet is not None:
            if isinstance(raw_packet, int):
                raw_packet = bytearray(raw_packet)
            self.raw_packet = raw_packet
            self.start, self.length = 0, len(raw_packet)
        elif packet_parameters != {}:
            minimum_packet_length = self.__class__.minimum_packet_length
            for name in packet_parameters.iterkeys():
                if self.__class__.elements_definitions_dict[name][1] is None:
                    minimum_packet_length += len(packet_parameters[name])
            self.raw_packet = bytearray(minimum_packet_length)
            self.start, self.length = 0, len(self.raw_packet)
            for name, value in packet_parameters.iteritems():
                setattr(self, name, value)


    def _get_element_substring(self, name):
        """Return a character or substring representing the named packet element"""
        start_position, length_or_code, end_position = self.__class__.elements_definitions_dict[name]
        start_position += self.start
        if start_position < 0:
            start_position += self.length
        if isinstance(length_or_code, str): #is a code
            return struct.unpack_from(length_or_code, buffer(self.raw_packet), start_position)[0]
        if length_or_code > 1: #must be int then
            return buffer(self.raw_packet, start_position, length_or_code)
        elif length_or_code is not None: #must be 1 then
            return chr(self.raw_packet[start_position])
        if end_position > 0:
            return buffer(self.raw_packet, start_position, end_position - start_position)
        elif end_position is not None: #must be negative then
            return buffer(self.raw_packet, start_position, self.length + end_position - start_position)
        

    def _set_element_substring(self, name, value):
        """Set the named packet element to a character or substring value"""
        start_position, length_or_code, end_position = self.__class__.elements_definitions_dict[name]
        start_position += self.start
        if start_position < 0:
            start_position += self.length
        if isinstance(length_or_code, str): #is a code
            struct.pack_into(length_or_code, self.raw_packet, start_position, value)
        elif length_or_code > 1: #must be int then
            self.raw_packet[start_position:start_position + length_or_code] = value
        elif length_or_code is not None: #must be 1 then
            self.raw_packet[start_position] = value
        elif end_position is not None: 
            self.raw_packet[start_position:end_position] = value
            

    def _del_element_substring(self, name):
        """Delete a character or substring in the raw_packet representing the named packet element"""
        length_or_code = self.__class__.elements_definitions_dict.pop(name)[1]
        if isinstance(length_or_code, str):
            self.__class__.minimum_packet_length -= struct.calcsize(length_or_code)
        elif length_or_code > 0: #so cannot be None
            self.__class__.minimum_packet_length -= length_or_code
            
        
    @classmethod
    def register_element(cls, name, docstring, start_position=None, code=None, end_position=None, set_function=None, length=None, get_function=None, del_function=None):
        """Register an element of the packet structure and make a :class:`property` for accessing a part of the packet with Packet.name  with a *docstring* which will either unpack or pack a value according to the *code* beginning at *start_position* or set or get a buffer starting at *start_position* and ending at *end_position* or provide your own *set_function*, *get_function* and *del_function*

        ::
        class RequestPacket(pydcpf.protocols.base.RequestPacket):
        ...
        RequestPacket.register_element('NUM', 'Number of bytes in the packet after NUM', 2, code='>H')
        RequestPacket.register_element('DATA','Data contained in the packet', 6, end_position=-2)

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
            index in the raw_packet buffer at which the value ends, in pythonic style
            mutually exclusive with *code*
            may be negative as an index relative to the end
        length : int, optional
            if the byte length cannot be deduced from *code* or *start_position* and *end_position* (e.g. if you specify your own functions or *end_position* is negative) it should be provided so :meth:`RequestPacket.__init__` allocates enough memory, otherwise it is calculated from the length of the provided arguments
        get_function : function, optional
            if not None, it will be used instead of creating one based on *start_position*, *code* or *end_position*
        set_function : function, optional
            if not None, it will be used instead of creating one based on *start_position*, *code* or *end_position*
        del_function : function, optional
            a function that safely deletes and unsets all instance attributes or dictionaries created by this property
            if *code* or *length* was specified, it should not be needed

        Note
        ----
        If you plan on using these properties to set the respective portions of the :attr:`ResponsePacket.raw_buffer`, it is your duty to make sure that the raw_buffer has enough space for the data
        """
        # first make sure the class variables are present
        try:
            cls.minimum_packet_length
        except AttributeError:
            cls.minimum_packet_length = 0
        try:
            cls.elements_definitions_dict
        except AttributeError:
            cls.elements_definitions_dict = {}

        length_or_code = None
        if code is not None:
            cls.minimum_packet_length += struct.calcsize(code)
            length_or_code = code
        elif length is not None:
            length_or_code = length
            cls.minimum_packet_length += length
        elif end_position is not None and end_position > 0:
            length_or_code = end_position - start_position
            cls.minimum_packet_length += length_or_code
        cls.elements_definitions_dict[name] = (start_position, length_or_code, end_position)
        if get_function is None:
            def get_function(self):
                return cls._get_element_substring(self, name)
        if set_function is None:
            def set_function(self, value):
                cls._set_element_substring(self, name, value)
        if del_function is None:
            def del_function(self):
                cls._del_element_substring(self, name)
        setattr(cls, name, property(fget=get_function, fset=set_function, fdel=del_function, doc=docstring))


    def __iter__(self):
        """Return and iterator over (element_name, value) pairs"""
        for name in self.__class__.elements_definitions_dict.iterkeys():
            yield (name, getattr(self, name))
            


class ResponsePacket(RequestPacket):
    """Response packet class

    This class should be used when receiving responses from the device

    For most protocols this class may be the same as :class:`RequestPacket`
    """


    def find(self):
        """Try to find a WHOLE packet in :attr:`ResponsePacket.raw_packet`

        This method must set :attr:`ResponsePacket.start` and :attr:`ResponsePacket.length`
        
        Returns
        -------
        found : bool
            True if a whole packet was found, False otherwise
        """
        pass


    def check(self, **parameters):
        """Check and verify the packet, optionally modify the verification method based on keyword *parameters*

        Parameters
        ----------
        **parameters : implementation dependant, optional
            keyword arguments possibly modifying the verification procedure

        Raises
        ------
        PacketException : implementation dependant
            Each protocol module defines its own exceptions
        """
        pass
