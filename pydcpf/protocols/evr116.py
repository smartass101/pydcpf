
from . import base

valid_command_characters = "hxyzijgpstv"


class RequestPacket(base.RequestPacket):


    def __init__(self, IDENTIFIER='v', DATA='?'):
        super(RequestPacket, self).__init__(IDENTIFIER=IDENTIFIER, DATA=DATA, TERMINATOR='\r\n')


    def find(self, buffer_start=0):
        raw_packet = self.raw_packet
        try:
            end = raw_packet.index('\r\n', buffer_start) + 1
        except ValueError:
            return False
        possible_start = raw_packet.rfind('\r\n', buffer_start, end - 1)
        if possible_start == -1:
            possible_start = buffer_start
        else:
            possible_start += 2
        for char in reversed(buffer(raw_packet, possible_start, end - possible_start - 1)):
            if char in valid_command_characters:
                self.start = raw_packet.rfind(char, possible_start, end - 2)
                self.length = end - self.start + 1
                return True
        return False



RequestPacket.register_element("IDENTIFIER", "initializing character identifying command", start_position=0, length=1)
RequestPacket.register_element("DATA", "data contained in packet", start_position=1, end_position=-2)
RequestPacket.register_element("TERMINATOR", "terminating characters", start_position=-2, length=2)

ResponsePacket = RequestPacket
