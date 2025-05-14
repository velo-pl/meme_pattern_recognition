#!/usr/bin/env python3.11
import json
import argparse
import os
import requests # For making direct API calls
import time

# It's good practice to use environment variables for API keys.
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YourApiKeyToken") # Default to placeholder if not set

def get_api_key(provided_key=None):
    """Helper function to get the API key."""
    if provided_key:
        return provided_key
    if ETHERSCAN_API_KEY != "YourApiKeyToken":
        return ETHERSCAN_API_KEY
    print("Warning: Etherscan API key not found. Please set the ETHERSCAN_API_KEY environment variable or provide it via --api_key argument. Using placeholder, API calls may fail.")
    return "YourApiKeyToken" # Fallback to placeholder

def fetch_etherscan_address_transactions(address: str, output_file: str, api_key_val: str, start_block: int = 0, end_block: int = 99999999, page: int = 1, offset: int = 100, sort: str = "asc"):
    """
    Fetches transaction history for a given Ethereum address using direct Etherscan API calls
    and saves it to a JSON file.
    """
    api_url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": start_block,
        "endblock": end_block,
        "page": page,
        "offset": offset,
        "sort": sort,
        "apikey": api_key_val
    }
    try:
        print(f"Fetching Etherscan transaction data for address: {address} via direct API call")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        if data.get("status") == "1" and data.get("message") == "OK":
            transactions = data.get("result", [])
            print(f"Successfully fetched {len(transactions)} transactions for address: {address}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(transactions, f, ensure_ascii=False, indent=4)
            print(f"Etherscan transaction data saved to {output_file}")
            return True
        elif data.get("message") == "NOTOK" and "Invalid API Key" in data.get("result", ""):
            print(f"Error: Invalid API Key. Please check your Etherscan API key.")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "Invalid API Key", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
            return False
        elif data.get("message") == "NOTOK" and "No transactions found" in data.get("result", ""):
            print(f"No transactions found for address: {address}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"message": "No transactions found", "address": address, "data": []}, f, ensure_ascii=False, indent=4)
            return True # Not an error, just no data
        elif data.get("message") == "NOTOK":
            print(f"Etherscan API Error for transactions: {data.get('result', 'Unknown error')}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "API Error", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
            return False
        else:
            print(f"Received unexpected response from Etherscan API for transactions: {data}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return False

    except requests.exceptions.RequestException as e:
        print(f"An HTTP error occurred while fetching Etherscan data for address '{address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "address": address}, f, ensure_ascii=False, indent=4)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while fetching Etherscan data for address '{address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "address": address}, f, ensure_ascii=False, indent=4)
        return False

def fetch_erc20_token_holders(contract_address: str, output_file: str, api_key_val: str, page: int = 1, offset: int = 100):
    """
    Fetches the list of ERC20 token holders for a given contract address using the Etherscan API (PRO endpoint).
    Saves the result to a JSON file.
    Note: This uses a PRO endpoint, which might be restricted on free API keys.
    """
    api_url = "https://api.etherscan.io/api"
    params = {
        "module": "token",
        "action": "tokenholderlist",
        "contractaddress": contract_address,
        "page": page,
        "offset": offset,
        "apikey": api_key_val
    }

    try:
        print(f"Fetching ERC20 token holder list for contract: {contract_address}")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        if data.get("status") == "1" and data.get("message") == "OK":
            holders = data.get("result", [])
            print(f"Successfully fetched {len(holders)} token holder records for contract: {contract_address}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(holders, f, ensure_ascii=False, indent=4)
            print(f"Token holder data saved to {output_file}")
            return True
        elif data.get("message") == "NOTOK" and "Invalid API Key" in data.get("result", ""):
            print(f"Error: Invalid API Key. Please check your Etherscan API key.")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "Invalid API Key", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
            return False
        elif data.get("message") == "NOTOK":
            print(f"Etherscan API Error for token holders: {data.get('result', 'Unknown error')}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "API Error", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
            return False
        else:
            print(f"Received unexpected response from Etherscan API for token holders: {data}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4) # Save the full response for inspection
            return False # Consider unexpected as failure for batch processing

    except requests.exceptions.RequestException as e:
        print(f"An HTTP error occurred while fetching token holder data for contract '{contract_address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "contract_address": contract_address}, f, ensure_ascii=False, indent=4)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while fetching token holder data for contract '{contract_address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "contract_address": contract_address}, f, ensure_ascii=False, indent=4)
        return False

def batch_fetch_etherscan_data(tasks_file: str, output_dir: str, api_key_val: str):
    """
    Processes a list of Etherscan data fetching tasks from a JSON file.
    Each task specifies the action (fetch_transactions or fetch_token_holders) and relevant parameters.
    """
    os.makedirs(output_dir, exist_ok=True)
    all_successful = True
    try:
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print(f"Error: Tasks file not found at {tasks_file}")
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from tasks file: {tasks_file}")
        return False

    for i, task in enumerate(tasks):
        action = task.get("action")
        output_filename_prefix = task.get("output_prefix", f"task_{i+1}")
        output_file = os.path.join(output_dir, f"{output_filename_prefix}.json")
        success = False

        print(f"\nProcessing task {i+1}/{len(tasks)}: action='{action}', output='{output_file}'")

        if action == "fetch_transactions":
            address = task.get("address")
            if not address:
                print(f"Skipping task {i+1}: 'address' not provided for fetch_transactions.")
                all_successful = False
                continue
            success = fetch_etherscan_address_transactions(
                address=address,
                output_file=output_file,
                api_key_val=api_key_val,
                start_block=task.get("start_block", 0),
                end_block=task.get("end_block", 99999999),
                page=task.get("page", 1),
                offset=task.get("offset", 100),
                sort=task.get("sort", "asc")
            )
        elif action == "fetch_token_holders":
            contract_address = task.get("contract_address")
            if not contract_address:
                print(f"Skipping task {i+1}: 'contract_address' not provided for fetch_token_holders.")
                all_successful = False
                continue
            success = fetch_erc20_token_holders(
                contract_address=contract_address,
                output_file=output_file,
                api_key_val=api_key_val,
                page=task.get("page", 1),
                offset=task.get("offset", 100)
            )
        else:
            print(f"Skipping task {i+1}: Unknown action '{action}'.")
            all_successful = False
        
        if not success:
            all_successful = False # Mark overall batch as not fully successful if any task fails
            print(f"Task {i+1} ('{action}') failed or returned no data. Check {output_file} for details.")
        else:
            print(f"Task {i+1} ('{action}') completed.")
        
        # Etherscan API rate limit is 5 calls/second for free tier, 10 calls/second for standard
        # Add a small delay to be safe, especially for batch processing.
        time.sleep(0.25) # 250ms delay, allows for up to 4 calls/sec
            
    return all_successful

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from Etherscan API. Can run in single mode or batch mode.")
    parser.add_argument("--api_key", type=str, default=None, help="Etherscan API Key. Overrides ETHERSCAN_API_KEY env var.")
    
    mode_parser = parser.add_subparsers(dest="mode", required=True, help="Operation mode")

    single_mode_parser = mode_parser.add_parser("single", help="Perform a single Etherscan action.")
    single_mode_parser.add_argument("-o", "--output_file", type=str, required=True, help="The path to the output JSON file for the single action.")
    action_subparsers = single_mode_parser.add_subparsers(dest="action", required=True, help="Action to perform")

    parser_tx = action_subparsers.add_parser("fetch_transactions", help="Fetch normal transaction history for an address.")
    parser_tx.add_argument("-a", "--address", type=str, required=True, help="The Ethereum address to query.")
    parser_tx.add_argument("--start_block", type=int, default=0, help="Starting block number.")
    parser_tx.add_argument("--end_block", type=int, default=99999999, help="Ending block number (default latest).")
    parser_tx.add_argument("--page", type=int, default=1, help="Page number for pagination.")
    parser_tx.add_argument("--offset", type=int, default=100, help="Number of transactions per page (max 10000).")
    parser_tx.add_argument("--sort", type=str, default="asc", choices=["asc", "desc"], help="Sort order for transactions.")

    parser_holders = action_subparsers.add_parser("fetch_token_holders", help="Fetch ERC20 token holder list for a contract address.")
    parser_holders.add_argument("-c", "--contract_address", type=str, required=True, help="The ERC20 token contract address.")
    parser_holders.add_argument("--page", type=int, default=1, help="Page number for pagination.")
    parser_holders.add_argument("--offset", type=int, default=100, help="Number of records per page.")

    batch_mode_parser = mode_parser.add_parser("batch", help="Process multiple tasks from a JSON file.")
    batch_mode_parser.add_argument("--tasks_file", type=str, required=True, help="Path to a JSON file containing a list of tasks.")
    batch_mode_parser.add_argument("--output_dir", type=str, required=True, help="Directory to save output files for batch tasks.")

    args = parser.parse_args()
    current_api_key = get_api_key(args.api_key)

    if args.mode == "single":
        if args.action == "fetch_transactions":
            fetch_etherscan_address_transactions(args.address, args.output_file, current_api_key, args.start_block, args.end_block, args.page, args.offset, args.sort)
        elif args.action == "fetch_token_holders":
            fetch_erc20_token_holders(args.contract_address, args.output_file, current_api_key, args.page, args.offset)
    elif args.mode == "batch":
        batch_fetch_etherscan_data(args.tasks_file, args.output_dir, current_api_key)

