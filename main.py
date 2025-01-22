import argparse
import logging
from src.parsers import LookupTableParser
from src.analyzer import FlowLogAnalyzer
from src.utils import write_output

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(description='Analyze VPC Flow Logs')
    parser.add_argument('log_file', help='Path to the flow log file')
    parser.add_argument('lookup_file', help='Path to the lookup table file')
    parser.add_argument('tag_output', help='Path to the tag counts output file')
    parser.add_argument('combo_output', help='Path to the port/protocol combination counts output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        lookup_table = LookupTableParser.parse(args.lookup_file)
        analyzer = FlowLogAnalyzer(lookup_table)
        tag_counts, port_protocol_counts = analyzer.analyze_file(args.log_file)
        
        write_output(tag_counts, args.tag_output, ['Tag', 'Count'])
        write_output(port_protocol_counts, args.combo_output, ['Port', 'Protocol', 'Count'])
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()