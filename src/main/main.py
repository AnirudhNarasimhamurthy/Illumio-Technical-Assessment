import argparse
from pathlib import Path
import logging
from datetime import datetime

from flow_logs_processor import process_flow_logs
from lookup_table_mapping_processor import load_lookup_table_mapping
from result_processor import write_results

# citation: some of the logging and main method skaffolding with input arguments was taken from previous experience
# working with it in the past to speed up the process of setting up the script

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Parse and tag Flow Logs based on port/protocol mappings')
    parser.add_argument('--flow-log-file', required=True, help='Flow log file')
    parser.add_argument('--mapping-file', required=True, help='Tags mapping or lookup table file')

    args = parser.parse_args()

    try:
        flow_path = Path(args.flow_log_file)
        mapping_path = Path(args.mapping_file)

        if not flow_path.exists() or not mapping_path.exists():
            logger.error("Input file(s) not found")
            return 1

        mappings = load_lookup_table_mapping(mapping_path)
        tag_counts, port_protocol_counts = process_flow_logs(flow_path, mappings)

        # Get project root directory (2 levels up from the script)
        project_root = Path(__file__).parent.parent.parent

        # Create output directory structure
        output_dir = project_root / 'output' / 'flow_logs'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f'flow_analysis_{timestamp}.csv'

        write_results(output_path, tag_counts, port_protocol_counts)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
