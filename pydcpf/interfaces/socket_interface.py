from . import base
import socket


class Interface(base.Interface):
    """Wrapper class around :class:`socket.socket`.

    Wrapping it is necessary because after disconnecting a new socket must be created when connecting again a nad also when serving

    Raises :class:`socket.timeout` error on timeout"""


    def _create_socket(self):
        self.socket = socket.socket(*self._socket_parameters)
        self.socket.settimeout(self._timeout)
    
    def __init__(self, timeout, family=socket.AF_INET, type=socket.SOCK_STREAM, protocol=0, _sock=None):
        self._socket_parameters = (family, type, protocol, _sock) # needed in disconnecting
        self._timeout = timeout
        self._create_socket()
        
    def connect(self, address, serve):
        if serve:
            self.socket.bind(address)
            self.socket.listen()
            self.socket = self.socket.accept()[0]
        else:
            self.socket.connect(address)
            

    def disconnect(self, address, serve):
        self.socket.close()
        self._create_socket()

    def send_data(self, data, flags=0):
        self.socket.sendall(data, flags)
        

    def receive_data(self, byte_count, flags=0):
        return self.socket.recv(byte_count, flags)
