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

"""API for the DAS1210 device made by Paouch s.r.o. used at the GOLEM reactor, FJFI, CVUT"""

from . import spinel_core
import struct


ranges = [0.25, 0.5, 1, 2.5, 5, 10]


class Device(spinel_core.Device):
    """Class representing the DAS1210 device

    Methods
    -------
    Almost all methods have a optional channel parameter
        this parameter determines the channel number ot operate on
        or (default value) operates on all channels otherwise (using the universal address).
    Where possible, the method parameters default to the values that are set on device reset.
    Methods beginning with 'set_'  return the DATA portion of the packet, usually empty
    Methods beginning with 'get_' return some meaningful value, see their docstring for more.
    """


    def __init__(self, ip_address, port=10001, **kwargs):
        """Initalize the device

        Parameters
        ----------
        ip_address : str
            IPv4 address of the device
        port : int, optional
            TCP port on which to initiate communication
            default is 10001
        **kwargs : keyword arguments
            these are passed on to :meth:`core.Device.__init__`
        """
        super(Device, self).__init__(address=(ip_address, port), protocol_module='pydcpf.protocols.spinel97', interface_module='pydcpf.interfaces.socket_interface', **kwargs)
    
    
    def set_range(self, value=10, channel=0xff):
        """Set the channel range.

        Parameters
        ----------
        value : int
            digitization range amplitude
            possible values [V]: 0.25, 0.5, 1, 2.5, 5, 10
            resulting range is from -value to +value
            
        Raises
        ------
        ValueError
            if specified range cannot be set (invalid value)
        """
        
        try:
            return self.query(INST='\x70', DATA=chr(ranges.index(value)), ADR=channel)
        except ValueError:
            raise ValueError("Invalid range specified, possible ranges are: " + repr(ranges))

        
    def get_range(self, channel):
        """Return the range of the channel in Volts.
        
        Inverse function to :func:`set_range`
        """
        try:
            return ranges[ord(str(self.query(INST='\x71', ADR=channel)))]
        except IndexError:
            raise ValueError("Device reports unexpected range with identifier " + value)

 
    def set_trigger(self, trigger=True, channel=0xff):
        """Set the trigger mode of the specified channel.

        Parameters
        ----------
        trigger : bool
            if True, use a rising edge trigger mode
            if False, use falling edge trigger mode
        """
        return self.query(INST='\x72', DATA=chr(int(trigger)), ADR=channel)


    def get_trigger(self, channel):
        """Return the trigger mode as bool as described in the inverse function :func:`set_trigger`
        """
        return bool(ord(str(self.query(INST='\x73', ADR=channel))))

    
    def set_sampling_frequency(self, freq=1e6, channel=0xff):
        """Set the sampling frequency of the specified channel.

        Parameters
        ----------
        freq : float
            freq for the specified channel in Hz
            ranges from 39.0625 kHz ('\xff') to 1.25 MHz ('\x07')
            default is 1 MHz
            the possible frequencies are given by the formula freq = 1e7 / (byte + 1)
            where byte ranges from '\x07' to '\xff'
            Therefore, the specified freq is rounded down to the nearest possible value.
        """
        return self.query(INST='\x74', DATA=chr(int(1e7 / freq) - 1), ADR=channel)


    def get_sampling_frequency(self, channel):
        """Return the sampling frequency for the specified channel in Hz as a float
        """
        return 1e7 / (ord(str(self.query(INST='\x75', ADR=channel)) + 1))


    def set_samples_count(self, count=524287, channel=0xff):
        """Set the number of samples to record by the specified channel.
        The actual number is rounded up to the closest multiple of 8.

        Parameters
        ----------
        count : int
            number of samples to set
            ranges from 0 to 524287 (default)
        """
        return self.query(INST='\x76', DATA=struct.pack('>i', count), ADR=channel)


    def get_samples_count(self, channel):
        """Return the number of samples that are recorded by the specified channel.
        Inverse function to :func:`set_samples_count`
        """
        return struct.unpack_from('>i', self.query(INST='\x77', ADR=channel))[0]


    def get_data(self, length, channel, packet_size=4096):
        """Retreive a data sample of the specified length from the specified channel.

        Parameters
        ----------
        length : int
            number of data points in sample
            should be a multiple of *packet_size*
        channel : int
            channel number
        packet_size : int
            number of data points to retreive in one packet
            defaults to 4096 which is the optimum value with regards to the device IO capabilities
            must not exceed 8192
            
        Returns
        -------
        data_array : list of buffers
            
        """
        target = [] #will append to the list
        packet_size_raw = struct.pack('>i', packet_size) #this needs to be done only once
        for packet_i in xrange(length / packet_size): #number of packets needed, rounded up to inlude the requested length for sure
            target.append(self.query(INST='\x51', DATA=struct.pack('>i', packet_i * packet_size) + packet_size_raw, ADR=channel))
        return target

    
    def get_data_ready(self, channel):
        """Return True if data are ready, False otherwise
        """
        return bool(ord(str(self.query(INST='\xf5', ADR=channel))))


    def set_ready(self, channel=0xff):
        """Set the specified channel operational.
        This must be done after the channel has recorded some data after trigger to empty the data memory buffer for the next measurement.
        """
        return self.query(INST='\x78', ADR=channel)


    def get_version(self):
        """Return a string describing the device and its version
        """
        return str(self.query(INST='\xf3', ADR=1))
