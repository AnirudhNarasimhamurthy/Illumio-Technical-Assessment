import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_lookup_table_mapping(mapping_file: Path) -> dict:
    # Load the mapping file and produce a dict/hashmap with dstport and protocol(string) as key and value as tag
    # for use while processing flow logs

    mappings = {}
    header = None
    with open(mapping_file, 'r') as f:
        first_line = True
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Assuming first line might be a header and if it is a header, it starts with dstport
            if first_line and line.startswith('dstport'):
                header = line.strip().split(',')
                first_line = False
                continue

            # If header doesn't exist in the file, then treat the first line as test
            first_line = False

            parts = line.split(',')
            if header is not None and len(parts) != len(header):
                logger.error(f'Invalid data: {line}')
                continue

            if len(parts) == 3:
                # Normalizing the casing for all string values for simpler lookups later
                dstport, protocol, tag = [p.strip().lower() for p in parts]
                key =(dstport, protocol)
                mappings[key] = tag

    logger.info(f'Finished loading {len(mappings)} mappings from lookup table mapping file')
    return mappings
