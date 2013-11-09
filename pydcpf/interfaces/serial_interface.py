from . import base
import serial



class Interface(base.Interface, serial.Serial):
    """Extended class of :class:`serial.Serial`.

    It only translates some of the method names and takes care of connecting on demand
    """


    def __init__(self, timeout, **kwargs):
        kwargs["timeout"] = timeout
        try:
            del kwargs["port"] #make sure the interface does not connect immediately
        except KeyError:
            pass                          #if port was not set, no problem
        super(Interface, self).__init__(**kwargs)
    
        
    def connect(self, address, serve):
        self.setPort(address)
        self.open()

        
    def disconnect(self, address, serve):
        self.close()

        
    def send_data(self, data):
        self.write(data)
        

    def receive_data(self, byte_count):
        return self.read(byte_count)
