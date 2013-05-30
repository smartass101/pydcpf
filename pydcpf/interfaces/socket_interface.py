from . import base
import socket

class Interface(socket.socket, base.Interface):
    def __new__(cls, *args, **kwargs):
        return super(Interface, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, protocol=0, _sock=None):
        super(Interface, self).__init__(family, type, protocol, _sock)
        
    def connect(self, address, serve):
        proxy = super(Interface,self)
        if serve:
            proxy.bind(address)
            proxy.listen()
            self = Interface(_sock=proxy.accept()[0])
        else:
            super(Interface, self).connect(address)

    def disconnect(self):
        super(Interface, self).close()

    def send_data(self, data, flags=0):
        super(Interface, self).sendall(data, flags)

    def receive_data(self, byte_count, flags=0):
        return super(Interface, self).recv(byte_count, flags)
