from . import base
import socket


class Interface(base.Interface):
    """Wrapper class around :class:`socket.socket`.

    Wrapping it is necessary because after disconnecting a new socket must be created when connecting again a nad also when serving"""

    
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, protocol=0, _sock=None):
        self._socket_parameters = (family, type, protocol, _sock) # meeded in disconnecting
        self.socket = socket.socket(self._socket_parameters)
        
        
    def connect(self, address, serve):
        if serve:
            self.socket.bind(address)
            self.socket.listen()
            self.socket = self.socket.accept()[0]
        else:
            self.socket.connect(address)
            

    def disconnect(self):
        self.socket.close()
        self.socket = socket.socket(self._socket_parameters)
        

    def send_data(self, data, flags=0):
        self.socket.sendall(data, flags)
        

    def receive_data(self, byte_count, flags=0):
        return self.socket.recv(byte_count, flags)
