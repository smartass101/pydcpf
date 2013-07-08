import unittest as ut
import pydcpf.protocols.spinel97 as s97

class TestSpinel97(ut.TestCase):
    
    def setUp(self):
        self.request_packet = s97.RequestPacket(INST='\x7f')
        self.response_packet = s97.ResponsePacket(ACK='\x00')
        
    def test_packet_init(self):
        self.assertEqual(self.request_packet.raw_packet, bytearray(b'*a\x00\x05\xfe\x02\x7f\xf0\r'))
        self.assertEqual(self.response_packet.raw_packet, bytearray(b'*a\x00\x05\xfe\x02\x00o\r'))

    def test_packet_checksum_error(self):
        self.response_packet.ADR = 5
        self.assertRaises(s97.CheckSumError, self.response_packet.check)
        self.request_packet.ADR = 11
        self.assertRaises(s97.CheckSumError, self.request_packet.check)

    def test_packet_ack_error(self):
        self.response_packet.ACK = '\x05'
        self.response_packet.SUMA = self.response_packet.calculate_checksum() # correct the checksum to prevent check raising CheckSumError 
        self.assertRaises(s97.ACKError, self.response_packet.check)
        try:
            self.request_packet.check() # should check out ok, ACK should not be reported
        except Exception as e:
            self.fail("request_packet.check() raised " + repr(e))


if __name__ == "__main__":
    ut.main()
