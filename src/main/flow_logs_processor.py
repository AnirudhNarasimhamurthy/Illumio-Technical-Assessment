import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Just adding the initial set of mapping for the protocol names that appear in the lookup file
# Additional mappings can be added based on the specification from here: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
PROTOCOL_MAP = {
    '1':  'icmp',
    '6':  'tcp',
    '17': 'udp',
}


# Convert protocol number to lowercase protocol name
def get_protocol_name(protocol_number: str) -> str:
    return PROTOCOL_MAP.get(protocol_number, f'unknown_{protocol_number}')


def process_flow_logs(log_file: Path, mappings: dict) -> tuple[dict, dict]:
    '''
    Process the flow logs and return the mappings
    :param log_file: flow log file
    :param mappings: mappings dict produced after parsing the lookup file
    :return: tuple of two dictionaries containing tag counts and port/protocol combination counts
    '''

    tag_counts = {'Untagged': 0}
    port_protocol_counts = {}
    parsing_errors = 0
    total_records = 0

    # Field positions (0-based index) in VPC flow logs
    dstport_index = 6
    protocol_index = 7
    with log_file.open('r') as f:
        '''
        Expected format: AWS VPC Flow Log version 2
        Example line format:
        2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK 
        Based on docs here: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html the 7th and 8th 
        fields are dstport and protocol which is what we are primarily interested in
        '''
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            # Assuming space as the delimiter based on the input provided in requirements. Update if needed
            fields = line.split()

            # Header detection and validation
            if line_number == 1:
                # Check if this might be a header (doesn't start with version number)
                if not fields[0].isdigit():
                    logger.info("Detected and skipping header row")
                    continue

            total_records += 1
            # Check if the line has enough fields to be a valid flow log entry
            if len(fields) < protocol_index:
                logger.warning(f"Skipping line {line_number} as it doesn't have enough fields")
                parsing_errors += 1
                continue

            try:
                # Extract dst port and the protocol number and name
                dstport = fields[dstport_index]
                protocol_number = fields[protocol_index]
                protocol_name = get_protocol_name(protocol_number)
                if protocol_name.startswith('unknown'):
                    logger.warning(f"Line {line_number}: Unknown protocol number: {protocol_number}")

                # Count port/protocol combinations
                port_protocol_key = (dstport, protocol_name)
                port_protocol_counts[port_protocol_key] = port_protocol_counts.get(port_protocol_key, 0) + 1

                # Look up and count tags
                mapping_key = (dstport, protocol_name)
                tag = mappings.get(mapping_key, 'Untagged')
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            except Exception as e:
                logger.warning(f"An error occurred while parsing/analayzing flow log from line {line_number} --> {str(e)}")
                parsing_errors += 1
                continue

        # Log processing summary
        logger.info(f"Processing complete:")
        logger.info(f"- Total records processed: {total_records}")
        logger.info(f"- Parsing errors: {parsing_errors}")

        if parsing_errors > 0:
            logger.warning(f"Found {parsing_errors} parsing errors out of {total_records} records processed.")

        return tag_counts, port_protocol_counts
