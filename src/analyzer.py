import os
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

        lookup_key = (
            0 if entry.protocol == Protocol.ICMP else entry.dst_port,
            entry.protocol.value
        )

        tag = self.lookup_table.get(lookup_key, 'Untagged')
        self.tag_counts[tag] += 1
        self.port_protocol_counts[lookup_key] += 1

    def analyze_file(self, file_path: str) -> Tuple[Dict[str, int], Dict[Tuple[int, str], int]]:
        try:
            with open(file_path, 'r', buffering=8192) as f:  # 8KB buffer
                # Only try to get file size for real files, not in test mode
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    processed_size = 0
                    last_report = 0

                for line in f:
                    if os.path.exists(file_path):
                        processed_size += len(line)
                        progress = (processed_size / file_size) * 100
                        if progress - last_report >= 5:
                            logger.info(f"Processed {progress:.1f}% of file")
                            last_report = progress

                    self.process_line(line)

            return dict(self.tag_counts), dict(self.port_protocol_counts)
            
        except FileNotFoundError:
            logger.error(f"Flow log file not found: {file_path}")
            raise