import unittest
from src.models import FlowLogEntry, Protocol

class TestFlowLogEntry(unittest.TestCase):
    def test_valid_flow_log_entry(self):
        log_line = "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK"
        entry = FlowLogEntry.from_log_line(log_line)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.version, 2)
        self.assertEqual(entry.dst_port, 49153)
        self.assertEqual(entry.protocol, Protocol.TCP)

    def test_invalid_version(self):
        log_line = "3 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK"
        entry = FlowLogEntry.from_log_line(log_line)
        self.assertIsNone(entry)

    def test_invalid_format(self):
        log_line = "invalid log entry"
        entry = FlowLogEntry.from_log_line(log_line)
        self.assertIsNone(entry)

    def test_protocol_mapping(self):
        protocols = {
            "6": Protocol.TCP,
            "17": Protocol.UDP,
            "1": Protocol.ICMP
        }
        
        for proto_num, expected in protocols.items():
            log_line = f"2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 {proto_num} 25 20000 1620140761 1620140821 ACCEPT OK"
            entry = FlowLogEntry.from_log_line(log_line)
            self.assertEqual(entry.protocol, expected)