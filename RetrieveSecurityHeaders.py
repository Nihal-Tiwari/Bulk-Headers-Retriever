import argparse
import pandas as pd
import requests
import json
from urllib.parse import urlparse
import sys

# Disable all requests and urllib3 warnings
requests.packages.urllib3.disable_warnings()

# Function to retrieve and return security response headers
def get_security_response_headers(url, disable_ssl_verify=False):
    try:
        # Check if the URL lacks a scheme (http or https) and add "https://"
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url

        # Set the user agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        # Determine whether to verify SSL certificates
        verify_ssl = not disable_ssl_verify

        response = requests.head(url, allow_redirects=True, headers=headers, verify=verify_ssl)
        final_url = response.url 
        status_code = response.status_code  

        # Print the status code
        print(f"URL: {final_url}, Status Code: {status_code}")

        if status_code == 200:
            # Specify the list of security headers to retrieve
            security_headers = [
                "strict-transport-security",
                "x-frame-options",
                "x-content-type-options",
                "content-security-policy",
                "x-permitted-cross-domain-policies",
                "referrer-policy",
                "clear-site-data",
                "cross-origin-embedder-policy",
                "cross-origin-opener-policy",
                "cross-origin-resource-policy",
                "cache-control",
                "permissions-policy"
            ]

            # Capture security response headers
            headers_dict = {header: response.headers.get(header, "HEADER_NOT_SET") for header in security_headers}

            return final_url, headers_dict, status_code
        else:
            return url, {"Status Code": status_code, "Error": "Failed to fetch headers"}, status_code
    except requests.exceptions.RequestException as e:
        return url, {"Error": str(e)}, None

def save_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Retrieve security headers and save to a file")
    parser.add_argument("input_file", help="Path to the input text file containing one website URL per line")
    parser.add_argument("output_file", help="Path to the output file where headers will be saved")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format (csv or json, default is csv)")
    parser.add_argument("--disable-ssl-verify", action="store_true", help="Disable SSL certificate verification")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    output_format = args.format
    disable_ssl_verify = args.disable_ssl_verify

    try:
        with open(input_file, 'r') as file:
            websites = file.read().splitlines()

        all_headers = []

        for website in websites:
            url, headers, status_code = get_security_response_headers(website, disable_ssl_verify)
            entry = {"URL": url, **headers, "Status Code": status_code}
            all_headers.append(entry)

            # Real-time printing of progress
            sys.stdout.write("\rRetrieving security headers... ")
            sys.stdout.flush()

        print("\nSecurity headers retrieved. Saving to file...")

        if output_format == "csv":
            save_to_csv(all_headers, output_file)
        elif output_format == "json":
            save_to_json(all_headers, output_file)

        print(f"Security headers saved to '{output_file}'")

    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
