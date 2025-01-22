from collections import defaultdict
from typing import Dict, Tuple, DefaultDict
import logging
from .models import FlowLogEntry, Protocol

logger = logging.getLogger(__name__)

class FlowLogAnalyzer:
    def __init__(self, lookup_table: Dict[Tuple[int, str], str]):
        self.lookup_table = lookup_table
        self.tag_counts: DefaultDict[str, int] = defaultdict(int)
        self.port_protocol_counts: DefaultDict[Tuple[int, str], int] = defaultdict(int)

    def process_line(self, line: str) -> None:
        entry = FlowLogEntry.from_log_line(line)
        if not entry:
            logger.debug(f"Skipping invalid line: {line.strip()}")
            return

        # Create lookup key based on destination port and protocol
        lookup_key = (
            0 if entry.protocol == Protocol.ICMP else entry.dst_port,
            entry.protocol.value
        )

        tag = self.lookup_table.get(lookup_key, 'Untagged')
        self.tag_counts[tag] += 1
        
        # Always count port/protocol combination, even if untagged
        self.port_protocol_counts[lookup_key] += 1

    def analyze_file(self, file_path: str) -> Tuple[Dict[str, int], Dict[Tuple[int, str], int]]:
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    self.process_line(line)
        except FileNotFoundError:
            logger.error(f"Flow log file not found: {file_path}")
            raise
            
        return dict(self.tag_counts), dict(self.port_protocol_counts)