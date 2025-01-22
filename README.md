# VPC Flow Log Analyzer

A Python tool to analyze AWS VPC Flow Logs and categorize network traffic based on destination ports and protocols using a lookup table.

## Features
- Analyzes AWS VPC Flow Logs (Version 2)
- Maps traffic to custom tags based on destination port and protocol combinations
- Generates two types of reports:
  - Tag counts: Shows how many times each tag appears
  - Port/Protocol combination counts: Shows traffic distribution across different ports and protocols
- Case-insensitive protocol matching
- Built-in logging for error tracking and debugging
- Support for ICMP, TCP, and UDP protocols

## Requirements
- Python 3.6+
- No external dependencies (uses standard library only)

## Project Structure
```
vpc-flow-analyzer/
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py      # Core analysis logic
│   ├── parsers.py      # File parsing logic
│   ├── models.py       # Data models/types
│   └── utils.py        # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_parsers.py
│   ├── test_models.py
│   └── test_utils.py
│
├── test_data/
│   ├── input/
│   │   ├── flow.log    # Sample flow log
│   │   └── lookup.csv  # Sample lookup table
│   └── expected/
│       ├── tag_counts.csv    # Expected tag counts
│       └── port_counts.csv   # Expected port counts
│
├── main.py
├── run_tests.py
└── README.md
```

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd vpc-flow-analyzer
```

## Usage
Run the script using the following command:
```bash
python main.py <flow_log_file> <lookup_table_file> <tag_output_file> <port_protocol_output_file>
```

### Arguments:
- `flow_log_file`: Path to the VPC Flow Log file
- `lookup_table_file`: Path to the CSV lookup table
- `tag_output_file`: Destination path for tag counts report
- `port_protocol_output_file`: Destination path for port/protocol counts report

### Example Usage:
```bash
python main.py test_data/input/flow.log test_data/input/lookup.csv output/tag_counts.csv output/port_counts.csv
```

### Input File Formats

1. Flow Log File:
   - Must be VPC Flow Log Version 2
   - Space-separated values
   - Example:
     ```
     2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
     ```

2. Lookup Table (CSV):
   - Headers: dstport,protocol,tag
   - Example:
     ```csv
     dstport,protocol,tag
     25,tcp,sv_P1
     68,udp,sv_P2
     443,tcp,sv_P2
     ```

### Output Files

1. Tag Counts (CSV):
   ```csv
   Tag,Count
   sv_P1,5
   sv_P2,3
   email,2
   Untagged,4
   ```

2. Port/Protocol Counts (CSV):
   ```csv
   Port,Protocol,Count
   25,tcp,2
   443,tcp,1
   68,udp,1
   ```

## Testing

### Running Unit Tests
Run the test suite:
```bash
python run_tests.py
```

For verbose output:
```bash
python -m unittest discover -v
```

### Test Data
Sample test data is provided in the `test_data/` directory:
- `input/`: Contains sample input files for testing
- `expected/`: Contains expected output files for verification

You can use these files to validate the program's functionality:
```bash
python main.py test_data/input/flow.log test_data/input/lookup.csv test_data/output/tag_counts.csv test_data/output/port_counts.csv
```

Then compare your outputs with the expected results in `test_data/expected/`.

## Error Handling and Logging
The program includes comprehensive error handling and logging:
- Invalid file formats
- Missing required fields
- Malformed data
- File access issues

Logs are output to console with appropriate error levels.

## Potential Improvements

1. Performance Optimizations:
   - Batch processing for large files
   - Memory-efficient processing for very large logs
   - Parallel processing support

2. Feature Additions:
   - Support for custom flow log formats
   - Source port/protocol analysis
   - Time-based analysis and reporting
   - Support for additional protocols
   - Configuration file support
   - Interactive mode for real-time analysis

3. Output Enhancements:
   - JSON output format
   - HTML report generation
   - Visualization of traffic patterns
   - Multiple output formats support

4. Error Handling:
   - More detailed error messages
   - Recovery mechanisms for corrupted files
   - Validation of input file formats

5. Testing:
   - Integration tests
   - Performance benchmarks
   - Test coverage improvements
   - Property-based testing

6. Documentation:
   - API documentation
   - More examples
   - Contributing guidelines
   - Changelog
