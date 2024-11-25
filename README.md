# Illumio-Technical-Assessment
All code related to technical assessment

# Flow Log Analyzer

Parses and analyzes AWS VPC Flow Logs based on destination port and protocol and produces a file/report containing
1. Count of matches for each tag
2. Count of matches for each port/protocol combination 

Assumptions or further validations that needs to be done have been left as comments in the code.

## Requirements
- Python 3.9+
- No additional packages needed

## Usage

Run the script main.py with the following arguments:

```
python main.py --flow-log-file <flow_log_file> --mapping-file <mapping_file>
```

The script will output a file named `flow_log_analysis_<timestamp>.csv` in the `output` folder under `flow_logs` directory.
The /output/ directory has been added to the .gitignore file to avoid uploading the output files to the repository.
