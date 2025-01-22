import csv
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def write_output(data: Dict[Any, int], file_path: str, headers: List[str]) -> None:
    try:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            # Sort items for consistent output
            for key, value in sorted(data.items()):
                if isinstance(key, tuple):
                    port, protocol = key
                    writer.writerow([port, protocol, value])
                else:
                    writer.writerow([key, value])
    except IOError as e:
        logger.error(f"Error writing to {file_path}: {e}")
        raise