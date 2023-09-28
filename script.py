import argparse
import pandas as pd
import requests
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to retrieve and return response headers for a given URL with SSL verification disabled
def get_response_headers_with_disabled_ssl_verification(url):
    try:
        # Set the user agent header to mimic Google Chrome
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        # Disable SSL verification
        response = requests.head(url, allow_redirects=True, verify=False, headers=headers)
        final_url = response.url 
        if response.status_code == 200:
            headers_dict = {}

            specific_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "Referrer-Policy",
                "Permissions-Policy"
            ]

            for header_name in specific_headers:
                header_value = response.headers.get(header_name, "Not set")
                headers_dict[header_name] = header_value

            return final_url, headers_dict
        else:
            return final_url, {"Status Code": response.status_code, "Error": "Failed to fetch headers"}
    except requests.exceptions.RequestException as e:
        return url, {"Error": str(e)}

def save_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Retrieve website headers and save to a file")
    parser.add_argument("input_file", help="Path to the input text file containing one website URL per line")
    parser.add_argument("output_file", help="Path to the output file where headers will be saved")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format (csv or json, default is csv)")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    output_format = args.format

    try:
        with open(input_file, 'r') as file:
            websites = file.read().splitlines()

        all_headers = []

        for website in websites:
            url, headers = get_response_headers_with_disabled_ssl_verification(website)
            all_headers.append({"URL": url, **headers})

        if output_format == "csv":
            save_to_csv(all_headers, output_file)
        elif output_format == "json":
            save_to_json(all_headers, output_file)

        print(f"Headers retrieved and saved to '{output_file}'")

    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

