"""API for the Quido IO module made by Papouch s.r.o."""

from .. import core
import struct 


outputs_count_fmts = {
    1 : 'B',
    2 : 'H',
    4 : 'I',
    }


class Device(core.Device):
    """Class representing a connected Quido module

    Communication is done through the Spinel 97 protocol,
    becuse it's more reliable than the Spinel 66 protocol
    """


    def __init__(self, inputs, outputs, **kwargs):
        super(Device, self).__init__(protocol_module='pydcpf.protocols.spinel97', **kwargs)


    def get_outputs_state(self, outputs_count):
        """Return the state of all outputs as a list

        Parameters
        ----------
        outputs_count : int
            number of outputs on the device
            the message structure is different for devices with 8, 16 and 32 outputs
        """
        data = self.query(INST='\x30')
        fmt = outputs_count_fmts[len(data)]
        return [ bool(int(i)) for i in bin(struct.unpack_from(fmt, data))[2:] ]

        
    def get_outputs_state(self, input_nr):
        input_nr -= 1
        return self.get_outputs_state((input_nr // 8 + 1) * 8)[input_nr]
    

    def set_outputs_states(self, *outputs_states):
        """
        outputs_states : list of ints
            output number to operate in,
            set axtive (high voltage) if positive,
            inactive (low voltage) if negative
        """
        return self.instruct(
            INST='\x20',
            DATA=struct.pack("%ib" % len(outputs_states),
                             # 1 bit H/L (-/+ bit) + 7 bits for output number from 1 to 127
                             *[ abs(i) if i < 0 else i - 128 for i in outputs_states ]),
            )

