import unittest
from unittest.mock import mock_open, patch
from io import StringIO
import csv
from src.parsers import LookupTableParser
from src.models import Protocol

class TestLookupTableParser(unittest.TestCase):
    def setUp(self):
        self.csv_data = StringIO(
            "dstport,protocol,tag\n"
            "25,tcp,sv_P1\n"
            "68,udp,sv_P2\n"
            "0,icmp,sv_P5\n"
        )

    @patch('builtins.open')
    def test_valid_lookup_table(self, mock_file):
        mock_file.return_value = self.csv_data
        lookup = LookupTableParser.parse('dummy.csv')
        
        self.assertEqual(len(lookup), 3)
        self.assertEqual(lookup[(25, Protocol.TCP)], 'sv_P1')
        self.assertEqual(lookup[(68, Protocol.UDP)], 'sv_P2')
        self.assertEqual(lookup[(0, Protocol.ICMP)], 'sv_P5')

    @patch('builtins.open')
    def test_invalid_csv_format(self, mock_file):
        invalid_csv = StringIO("bad,format\nno,headers\n")
        mock_file.return_value = invalid_csv
        
        with self.assertRaises(KeyError):
            LookupTableParser.parse('invalid.csv')