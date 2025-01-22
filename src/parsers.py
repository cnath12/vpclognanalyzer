import csv
from typing import Dict, Optional
import logging
from .models import Protocol, LookupKey

logger = logging.getLogger(__name__)

class LookupTableParser:
    REQUIRED_HEADERS = {'dstport', 'protocol', 'tag'}

    @staticmethod
    def parse(file_path: str) -> Dict[LookupKey, str]:
        lookup = {}
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                if not all(header in reader.fieldnames for header in LookupTableParser.REQUIRED_HEADERS):
                    missing = LookupTableParser.REQUIRED_HEADERS - set(reader.fieldnames or [])
                    raise KeyError(f"Missing required headers: {missing}")

                for row in reader:
                    try:
                        port = int(row['dstport'])
                        protocol = row['protocol'].lower()
                        tag = row['tag']
                        lookup[(port, protocol)] = tag
                    except (ValueError, KeyError) as e:
                        logger.warning(f"Skipping invalid lookup entry: {row}. Error: {e}")
        except FileNotFoundError:
            logger.error(f"Lookup table file not found: {file_path}")
            raise
        except csv.Error as e:
            logger.error(f"Error parsing lookup table: {e}")
            raise
            
        return lookup