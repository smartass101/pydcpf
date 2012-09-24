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
            If None, the bytes will not be split into chunks
        receive_byte_count : int or None, optional
            Size of byte chunks to receive at once
            If None, the bytes will not be split into chunks
        connect : bool, optional
            If True, connect immediately after initialization
        serve : bool, optional
            If True, this device is expected to wait for a connection which may modify the way the device connects
        """
        self.serve = serve
        self.address = address
        self.send_byte_count = send_byte_count
        self.receive_byte_count = receive_byte_count
        if not isinstance(protocol_module, ModuleType):
            protocol_module = __import__(protocol_module, fromlist=[''])
        self.protocol = protocol_module
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
        if address is None:
            address = self.address
        if serve is None:
            serve = self.serve
        self.interface.connect(address, serve)

    def serve(self): #useful?
        pass

    def send_request_packet(self, packet):
        pass

    def receive_response(self, **kwargs):
        """get a packet and return only data, but check the packet first"""
        pass

    def receive_response_packet(self, packet):
        pass

    def query(self): #useful ? just calling two functions
        pass
    
