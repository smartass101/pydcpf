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
"""API for the Quido IO module made by Papouch s.r.o."""

from .. import core
import struct 


_outputs_inputs_count_fmts = {
    1 : 'B',
    2 : 'H',
    4 : 'I',
    }


class Device(core.Device):
    """Class representing a connected Quido module

    Communication is done through the Spinel 97 protocol,
    becuse it's more reliable than the Spinel 66 protocol
    """


    def __init__(self, address, **kwargs):
        super(Device, self).__init__(address, protocol_module='pydcpf.protocols.spinel97', **kwargs)


    def _decode_inputs_outputs_state(self, data):
        """Common code for decoding responses
        describing inputs or outputs state

        Note
        ----
            only for max 32 inputs/outputs
        """
        data_len = len(data)
        fmt = _outputs_inputs_count_fmts[data_len]
        state = [ bool(int(i)) for i in
              ("%0" + "%ii" % 8**data_len) % int(bin(struct.unpack_from(fmt, data)[0])[2:]) # crunch down to padded binary string representation
              ]
        state.reverse()        # reverse in place as specified in docs
        return state


    def get_outputs_state(self, address):
        """Return the state of all outputs as a list
        on the device with the specified address

        Returns
        -------
        outputs_state : list of bool
            length depends of number of outputs on device
            True if active (high voltage)
            False if inactive (low voltage)
        """
        return self._decode_inputs_outputs_state(
            self.query(INST='\x30', ADR=address)
            )

        
    def get_output_state(self, output_number, address):
        """Return the state of output given by *output_number*
        on the device with the specified address

        Returns
        -------
        output_state : bool
            

        Note
        ----
        This method has to call :meth:`Device.get_outputs_state`
        to get the status of all outputs first anyways,
        so it's more resourceful to batch output querying
        """
        return self.get_outputs_state(address)[output_number - 1] # list indexed from 0
    

    def set_outputs_state(self, address, *outputs_state):
        """
        Set each specified output to the given state

        Parameters
        ----------
        outputs_state : list of ints
            output numbers to operate on,
            set active (high voltage) if positive,
            inactive (low voltage) if negative
            no order is required, arbitrary outputs can be given
        """
        return self.query(
            INST='\x20',
            DATA=struct.pack("%ib" % len(outputs_state),
                             # 1 bit H/L (-/+ bit) + 7 bits for output number from 1 to 127
                             *[ abs(i) if i < 0 else i - 128 for i in outputs_state ]),
            )


    def get_inputs_state(self, address):
        """Return the state of all inputs as a list
        on the device with the specified address

        Returns
        -------
        inputs_state : list of bool
            length depends of number of inputs on device
            True if active (high voltage)
            False if inactive (low voltage)
        """
        return self._decode_inputs_outputs_state(
            self.query(INST='\x31', ADR=address)
            )
