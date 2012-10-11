"""This module provides the core class of the package: :class:`Device`"""

from types import ModuleType

class Device(object):
    """Core class used for communication with a device

    Uses a subclass of :class:`interfaces.base.Interface` class for data transmission and sublcasses of :class:`protocols.base.RequestPacket` and :class:`protocols.base.ResponsePacket` for data encoding and decoding respectively.
    """
    def __init__(self, address, protocol_module, interface_module=None, send_byte_count=8192, receive_byte_count=8192, connect=True, serve=False, **interface_kwargs):
        """Initialize the device

        Parameters
        ----------
        address : interface dependant
            The address of the physical device used to create the underlying interface
            if the *interface_module* is not specified, pydcpf.interfaces.serial module is used if address is a str or int referencing a serial port (e.g. '/dev/ttyUSB0', '/dev/ttyS0' or a number of the serial/COMM port) or the pydcpf.interfaces.socket module is used if address is a tuple of (str, int) (e.g. ('192.168.1.254', 10001)) for Interface creation.
        protocol_module : str or module
            From where to load the packet classes, the module must provide a ResponsePacket and RequestPacket class (for many protocols they are the same)
        interface_module : str or module, optional
            From where to load the Interface class
            If not specified, the module is guessed from the *address* parameter
        send_byte_count : int or None, optional
            Size of byte chunks to send at once
            If 0, the bytes will not be split into chunks
        receive_byte_count : int or None, optional
            Size of byte chunks to receive at once
            If 0, the bytes will not be split into chunks
        connect : bool, optional
            If True, connect immediately after initialization
        serve : bool, optional
            If True, this device is expected to wait for a connection which may modify the way the device connects
        """
        self.data_buffer = bytearray()
        self.serve = serve
        self.address = address
        self.send_byte_count = send_byte_count
        self.receive_byte_count = receive_byte_count
        if not isinstance(protocol_module, ModuleType):
            protocol_module = __import__(protocol_module, fromlist=[''])
        self.protocol = protocol_module
        self._request_buffer_packet = protocol_module.RequestPacket()
        if interface_module: #was explicitely specified
            if not isinstance(interface_module, ModuleType):
                interface_module = __import__(interface_module, fromlist=[''])
        else:
            if isinstance(address, (int, str)): #seems to be a serial device
                interface_module = __import__('pydcpf.interfaces.serial')
            elif isinstance(address, tuple) and len(address) == 2 and isinstance(address[0], str) and isinstance(address[1], int): #appears to be a scoket address
                interface_module = __import__('pydcpf.interfaces.socket')
        self.interface = interface_module.Interface(**interface_kwargs)
        if connect:
            self.connect()
        
    def connect(address=None, serve=None):
        """Connect the device, optionally override the Device.address ad Device.serve attributes (same form and meaning as in :meth:`Device.__init__`)"""
        if address is None:
            address = self.address
        if serve is None:
            serve = self.serve
        self.interface.connect(address, serve)

    def serve(self): #useful?
        pass


    def send_request_packet(self, packet, send_byte_count=None):
        """Send a request packet, optionally send *send_byte_count* size byte chunks at once

        Parameters
        ----------
        packet : RequestPacket
            packet to send
        send_byte_count : int, optional
            if specified, this will override the Device.send_byte_count attribute specified during initialization
        """
        if send_byte_count is None:
            send_byte_count = self.send_byte_count
        raw_packet = packet.raw_packet
        if send_byte_count == 0: #do not split the packet TODO possibly to loose checking, what about None or negative values?
            self.interface.send_data(raw_packet)
        else: #may split
            for delimiter in xrange(0, len(raw_packet), send_byte_count):
                self.interface.send_data(raw_packet[delimiter:delimiter + send_byte_count])
                
    def send_request(self, send_byte_count=None, **packet_parameters):
        """Send a request, optionally send *send_byte_count* size byte chunks at once

        Parameters
        ----------
        send_byte_count : int, optional
            if specified, this will override the Device.send_byte_count attribute specified during initialization
        **packet_parameters
            keyword arguments containing parameters for packet creation
        """
        self.send_request_packet(self._request_buffer_packet.__init__(**packet_parameters), send_byte_count)
            

    def receive_response(self, receive_byte_count=None, **check_parameters):
        """Receive a response and return only data, but check the packet first

        """
        packet = self.receive_response_packet(receive_byte_count)
        packet.check(**check_parameters)
        return packet.data

    def receive_response_packet(self, receive_byte_count=None, packet=None):
        """Receive a response and return the received packet, optionally read *receive_byte_count* sized byte chunks at once into the specified *packet*

        Parameters
        ----------
        receive_byte_count : int, optional
            if specified, this will override the Device.receive_byte_count attribute specified during initialization
        packet : ResponsePacket, optional
            If specified, the data will be read into this packet and then it will be returned

        Returns
        -------
        packet : ResponsePacket
            Packet created from the protocol module (specified during initialization) or the one passed to this method
        """
        if packet is None:
            packet = self.protocol.ResponsePacket()
        if receive_byte_count is None:
            receive_byte_count = self.receive_byte_count
        packet.raw_packet = self.data_buffer
        while not packet.find():
            packet.raw_packet.extend(self.interface.receive_data(receive_byte_count))
        self.data_buffer = packet.raw_packet[packet.start + packet.length:]
        return packet
    
    def query(self): #useful ? just calling two methods
        pass
    

class Server(object):
    """Serves Devices

    Has the ability to find out protocol they want to use for communication
    """
    pass
