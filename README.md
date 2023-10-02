# Website Security Headers Retriever Tool

This tool allows you to retrieve security response headers from a list of website URLs and save the results to a CSV or JSON file. It is useful for analyzing the security headers of various websites.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Output](#output)
- [Examples](#examples)

## Prerequisites

Before using this script, make sure you have the following prerequisites installed:

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - pandas

## Getting Started

1. Clone this repository to your local machine or download the script file (`RetrieveSecurityHeaders.py`) directly.
2. Install the required Python packages using the command: pip install -r requirements.txt


## Usage

To use the script, follow these steps:

1. Create a text file (`input.txt`) containing one website URL per line that you want to analyze.
2. Run the RetrieveSecurityHeaders.py with the following command:

python RetrieveSecurityHeaders.py input.txt output.csv --format csv

- `input.txt`: Path to the input file with the list of website URLs.
- `output.csv`: Path to the output file where headers will be saved. You can change the format to JSON by specifying `--format json`.
- The default format is CSV.

## Output

The script retrieves the following security response headers for each website:

- strict-transport-security
- x-frame-options
- x-content-type-options
- content-security-policy
- x-permitted-cross-domain-policies
- referrer-policy
- clear-site-data
- cross-origin-embedder-policy
- cross-origin-opener-policy
- cross-origin-resource-policy
- cache-control
- permissions-policy

The headers are saved in the specified output file in CSV or JSON format.

## Examples

- For CSV File:
  
python website_security_headers.py input.txt output.csv --format csv

- For JSON file:
  
python website_security_headers.py input.txt output.json --format json

- For Default Format (CSV) :

python website_security_headers.py input.txt output.csv

