import unittest
from unittest.mock import mock_open, patch
import csv
from io import StringIO
from src.utils import write_output
from src.models import Protocol

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.tag_counts = {
            'sv_P1': 2,
            'sv_P2': 1,
            'Untagged': 3
        }
        self.port_protocol_counts = {
            (25, Protocol.TCP): 2,
            (68, Protocol.UDP): 1
        }

    @patch('builtins.open')
    def test_write_tag_counts(self, mock_open_):
        mock_file = StringIO()
        mock_open_.return_value.__enter__.return_value = mock_file
        
        write_output(self.tag_counts, 'output.csv', ['Tag', 'Count'])
        
        mock_file.seek(0)
        reader = csv.DictReader(mock_file)
        written_data = {row['Tag']: int(row['Count']) for row in reader}
        
        self.assertEqual(written_data, self.tag_counts)