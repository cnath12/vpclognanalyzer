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
            (25, 'tcp'): 2,
            (68, 'udp'): 1
        }

    @patch('builtins.open')
    def test_write_tag_counts(self, mock_open_):
        mock_file = StringIO()
        mock_open_.return_value.__enter__.return_value = mock_file
        
        with patch('os.makedirs') as mock_makedirs:  # Mock makedirs
            write_output(self.tag_counts, './output/test.csv', ['Tag', 'Count'])
            
            # Verify makedirs was called with correct path
            mock_makedirs.assert_called_once_with('./output', exist_ok=True)
        
        mock_file.seek(0)
        reader = csv.DictReader(mock_file)
        written_data = {row['Tag']: int(row['Count']) for row in reader}
        
        self.assertEqual(written_data, self.tag_counts)

    @patch('builtins.open')
    def test_write_to_current_directory(self, mock_open_):
        mock_file = StringIO()
        mock_open_.return_value.__enter__.return_value = mock_file
        
        # Should not raise any error when writing to current directory
        write_output(self.tag_counts, 'test.csv', ['Tag', 'Count'])
        
        mock_file.seek(0)
        reader = csv.DictReader(mock_file)
        written_data = {row['Tag']: int(row['Count']) for row in reader}
        
        self.assertEqual(written_data, self.tag_counts)