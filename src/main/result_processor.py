import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_results(output_file: Path, tag_counts: dict, port_protocol_counts: dict):
    """
    Write the results to the output file
    :param output_file:
    :param tag_counts: dict/map containing tag counts
    :param port_protocol_counts: dict/map containing port/protocol counts
    :return: file containing information about tag counts and port/protocol counts in a comma separated format
    """
    with open(output_file, 'w') as f:
        logger.info(f"Writing results for tag counts to output file: {output_file}")
        f.write("Tag counts:\n\n")
        f.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            f.write(f"{tag},{count}\n")

        f.write("\n\n=========================================\n\n")
        f.write("Port protocol combination counts:\n\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            f.write(f"{port},{protocol},{count}\n")


    logger.info("Results written successfully. Processing complete.")
