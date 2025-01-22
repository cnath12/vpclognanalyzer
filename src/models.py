from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

class Protocol(str, Enum):
    TCP = 'tcp'
    UDP = 'udp'
    ICMP = 'icmp'

# Add back the LookupKey type
LookupKey = Tuple[int, str]  # (port, protocol)

@dataclass
class FlowLogEntry:
    version: int
    dst_port: int
    protocol: Protocol
    
    @classmethod
    def from_log_line(cls, line: str) -> Optional['FlowLogEntry']:
        try:
            fields = line.strip().split()
            if len(fields) < 14 or fields[0] != '2':
                return None
            
            protocol_map = {6: Protocol.TCP, 17: Protocol.UDP, 1: Protocol.ICMP}
            protocol = protocol_map.get(int(fields[7]), Protocol.TCP)
            
            return cls(
                version=int(fields[0]),
                dst_port=int(fields[6]),
                protocol=protocol
            )
        except (IndexError, ValueError):
            return None