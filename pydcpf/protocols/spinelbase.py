from .base import ResponsePacket


class ACKError(Exception):
    """Acknowledgment code error

    Attributes
    ----------
    ACK : str
        Acknowledgment code in the packet
    """

    descriptions = {
            0x00 : "OK",
            0x01 : "Unknown error",
            0x02 : "Invalid instruction",
            0x03 : "Invalid instruction parameters",
            0x04 : "Permission denied", #write error, too low data, channel disabled, other requirements not met
            0x05 : "Device malfunction",
            0x06 : "Data not available",
            0x0d : "Digital input state change", #automatically sent message
            0x0e : "Continuous measurement", #automatically sent, repeatedly sending measured data
            0x0f : "Range overrun" #automatically sent
        }
    
    def __init__(self, ACK_code):
        self.ACK = ACK_code
        
    def __str__(self):
        try:
            int_ACK = int(self.ACK, 16)
        except ValueError: #must be something like '\x0d', so use ord
            int_ACK = ord(self.ACK)
        return "Non-zero acknowledgment code " + hex(int_ACK) + ": " + self.__class__.descriptions[int_ACK]

    
class SpinelBasePacket(ResponsePacket):
    def find(self):
        raw_packet = self.raw_packet
        start = raw_packet.find('*')
        if start == -1:
            return False
        end = raw_packet.find('\r', start)
        if end == -1:
            return False
        start = raw_packet.rfind('*', start, end)
        self.start, self.length = start, end - start + 1
        return True

SpinelBasePacket.register_element('PRE', "Packet prefix character", start_position=0, length=1)
SpinelBasePacket.register_element('FRM', "Packet format number", start_position=1, code='>B')
SpinelBasePacket.register_element('CR', "Ending mark character", start_position=-1, length=1)
