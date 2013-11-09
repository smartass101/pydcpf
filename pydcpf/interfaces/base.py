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
"""This module provides the base :class:`Interface` class for documentation purposes."""

__all__ = ['Interface']


class Interface(object):
    """Base class for device data transmission"""

    
    def __init__(self, timeout, **kwargs):
        """Initialize the interface using the keyword arguments (implementation dependent).

        The timout argument represents a timout in seconds for connecting, reading writing. If 0, no timeout should be set. The timeout error raised on timout is implementation dependent.

        The interface must not connect immediately after initialization, :meth:`Interface.connect` must be used for that.
        """
        pass


    def connect(self, address, serve):
        """Connect the interface to the address specified, possibly in a special way if serving.
        
        Parameters
        ----------
        address
                The type and content depends on the implementation.
        server : bool
            May modify the behavior of the method depending on the implementation, e.g. if True, :meth:`Interface.connect` may wait for a connection on *address*, if False, it may request a connection from *address*.
            For simpler interfaces, the server and client behavior may be the same.      
        """
        pass


    def disconnect(self, address, serve):
        """Disconnect the interface, possibly in a special way if serving.
        
         Parameters
        -----------
        server : bool
            May modify the behavior of the method depending on the implementation, e.g. if True, :meth:`Interface.disconnect` may take a few more action to clean up the interface properly.
            For simpler interfaces, the server and client behavior may be the same.      """
        pass
    

    def send_data(self, data):
        """Sends the data through the interface.

        Parameters
        ----------
        data : str or bytearray or bytes
            data to be sent

        Note
        ----
        This method is expected to send *ALL* data, so it may have to check whether all data was sent
        """
        pass
    

    def receive_data(self, byte_count):
        """Receive up to byte_count bytes from the interface and return them

        Parameters
        ----------
        byte_count : int
            number of bytes to attempt to read, may return equal or less

        Return
        ------
        data : str or bytearray, or bytes
            received data
        """
        pass
    
        
