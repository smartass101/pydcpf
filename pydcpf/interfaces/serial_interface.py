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
