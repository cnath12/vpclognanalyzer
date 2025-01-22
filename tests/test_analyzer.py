import unittest
from unittest.mock import mock_open, patch
from src.analyzer import FlowLogAnalyzer
from src.models import Protocol

class TestFlowLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.lookup_table = {
            (25, Protocol.TCP): 'sv_P1',
            (68, Protocol.UDP): 'sv_P2',
            (0, Protocol.ICMP): 'sv_P5'
        }
        self.analyzer = FlowLogAnalyzer(self.lookup_table)

    def test_process_valid_line(self):
        line = "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 25 6 25 20000 1620140761 1620140821 ACCEPT OK"
        self.analyzer.process_line(line)
        
        self.assertEqual(self.analyzer.tag_counts['sv_P1'], 1)
        self.assertEqual(self.analyzer.port_protocol_counts[(25, Protocol.TCP)], 1)

    def test_analyze_file(self):
        mock_content = "\n".join([
            "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 25 6 25 20000 1620140761 1620140821 ACCEPT OK",
            "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 68 17 25 20000 1620140761 1620140821 ACCEPT OK",
            "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 80 6 25 20000 1620140761 1620140821 ACCEPT OK"
        ])
        
        with patch('builtins.open', mock_open(read_data=mock_content)):
            tag_counts, port_protocol_counts = self.analyzer.analyze_file('dummy.log')
        
        self.assertEqual(tag_counts['sv_P1'], 1)
        self.assertEqual(tag_counts['sv_P2'], 1)
        self.assertEqual(tag_counts['Untagged'], 1)