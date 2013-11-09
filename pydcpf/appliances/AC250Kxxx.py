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
from .. import core


class Device(core.Device):
    """Device representing a AC250Kxxx series power supply by Diametral

    Communications goes over a serial line with a baudrate of 9600, bytesize of 8, no bit parity, 1 stopbit and no flow control
    """


    def __init__(self, serial_port, address=0xff, **kwargs):
        """Initialize a new Device object with the specified address communicating through the specified serial port.

        Parameters
        ----------
        serial_port : int or str
            number of the serial port to be used for communication
            or the explicit name of the device to be passed to :meth:`serial.Serial.__init__`
            on Linux it's the number X in /dev/ttySX and defaults to 0 (/dev/ttyS0)
        address : int, optional
            internal device address
            ranges from 0 to 31 inclusive, defaluts to 255 (broadcast address)
            address 255 is the broadcast address, any device accepts it, but won't send a response packet back (not recommended, makes debugging very hard)
            the device address can be displayed by holding the red 'Clear' button for several seconds
        kwargs : keyword arguments dict
            passed on to :meth:`core.Device.__init__`
        """
        self.internal_address = address
        super(Device, self).__init__(address=serial_port, interface_module="pydcpf.interfaces.serial_interface",
                                     protocol_interface="pydcpf.protocols.AC250Kxxx",
                                     baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=False)


    def query(self, send_byte_count=None, receive_byte_count=None, check_parameters=dict(), **packet_parameters):
        """Wrapper around :meth:`core.Device.query` taht inserts the internals address if none is specified"""
        if not "ADR" in packet_parameters:
            packet_parameters["ADR"] = self.internal_address
        super(Device, self).query(send_byte_count, receive_byte_count, check_parameters, **packet_parameters)
        
            
    def command(self, send_byte_count=None, receive_byte_count=None, check_parameters=dict(), **packet_parameters):
        """Device.command(instruction) -> ack

        Send a command to the device and wait for acknowledgment (ACK)
        Essentially just a wrapper around :meth:`Device.query`

        Parameters
        ----------
        same as for :meth:`Device.query`

        Returns
        -------
        ack : bool
            True if Device replied 'OK'
            False if Device replied 'Err'
            
        Raises
        ------
        :class:`RuntimeError`
            Raises if the reply was something else than 'OK' or 'Err'
        """
        ack = self.query(send_byte_count, receive_byte_count, check_parameters, **packet_parameters)
        if ack == 'OK':
            return True
        elif ack == 'Err':
            return False
        else:
            raise RuntimeError("Device reported error: " + ack)

        
    def get_voltage(self):
        """Device.get_voltage() -> voltage

        Return the current set voltage in Volts

        Returns
        -------
        voltage : int
            current voltage in Volts
        """
        return int(self.query(DATA='NAP???')[3:]) #reply is 'NAPXXX'

        
    def set_voltage(self, voltage):
        """Device.set_voltage(voltage) -> success

        Set the voltage in Volts

        Parameters
        ----------
        voltage : int
            voltage to set in Volts

        Returns
        -------
        success : bool
            True if the command did succeed, False otherwise
        """
        return self.command(DATA=('NAP%03d' % voltage)) #it takes some time for the voltage to change

        
    voltage = property(fget=get_voltage, fset=set_voltage, doc="""Output voltage as an integer in Volts""")

    
    def get_output(self):
        """Device.get_output() -> status

        Return the current status of the output

        Returns
        -------
        status : bool
            True if output is activated, False otherwise
        """
        if self.query(DATA='OUT?')[-1] == '1': #should be 'OUT1'
            return True
        else: #should be 'OUT0'
            return False

        
    def set_output(self, status):
        """Device.set_output(status) -> success

        Set the status of the output

        Parameters
        ----------
        status : bool
            True if output should be activated, False otherwise
        
        Returns
        -------
        success : bool
            True if the command did succeed, False otherwise
        """
        if status: #if True
            return self.command(DATA='OUT1')
        else:
            return self.command(DATA='OUT0')

        
    output = property(fget=get_output, fset=set_output, doc="""Output status as a Boolean, True if activated, False otherwise""")
    
        
    def get_identification(self):
        """Device.get_identification() -> identification

        Return the identification of the device

        Returns
        -------
        identification : str
            name of the device, model and revision
        """
        return self.query(DATA='ID?')

    identification = property(fget=get_identification, doc="""Device identifiaction as a string""")
        
