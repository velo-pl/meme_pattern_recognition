#!/usr/bin/env python3.11
import json
import argparse
import os
import requests # For making direct API calls if library doesn't support endpoint
from etherscan import Etherscan # Import the installed library

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
    Fetches transaction history for a given Ethereum address using the Etherscan API
    and saves it to a JSON file.
    """
    try:
        eth = Etherscan(api_key_val) 
        print(f"Fetching Etherscan transaction data for address: {address}")
        
        transactions = eth.get_normal_txs_by_address(
            address=address,
            startblock=start_block,
            endblock=end_block,
            page=page,
            offset=offset,
            sort=sort
        )

        if transactions:
            print(f"Successfully fetched {len(transactions)} transactions for address: {address}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(transactions, f, ensure_ascii=False, indent=4)
            print(f"Etherscan transaction data saved to {output_file}")
        else:
            print(f"No transactions found or returned from Etherscan API for address: {address}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"message": "No transactions found or returned", "address": address, "data": []}, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred while fetching Etherscan data for address 	'{address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "address": address}, f, ensure_ascii=False, indent=4)

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
        elif data.get("message") == "NOTOK" and "Invalid API Key" in data.get("result", ""):
            print(f"Error: Invalid API Key. Please check your Etherscan API key.")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "Invalid API Key", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
        elif data.get("message") == "NOTOK":
            print(f"Etherscan API Error for token holders: {data.get('result', 'Unknown error')}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "API Error", "message": data.get("result")}, f, ensure_ascii=False, indent=4)
        else:
            print(f"Received unexpected response from Etherscan API for token holders: {data}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4) # Save the full response for inspection

    except requests.exceptions.RequestException as e:
        print(f"An HTTP error occurred while fetching token holder data for contract 	'{contract_address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "contract_address": contract_address}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"An unexpected error occurred while fetching token holder data for contract 	'{contract_address}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "contract_address": contract_address}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from Etherscan API.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="The path to the output JSON file.")
    parser.add_argument("--api_key", type=str, default=None, help="Etherscan API Key. Overrides ETHERSCAN_API_KEY env var.")
    
    subparsers = parser.add_subparsers(dest="action", required=True, help="Action to perform")

    # Subparser for fetching address transactions
    parser_tx = subparsers.add_parser("fetch_transactions", help="Fetch normal transaction history for an address.")
    parser_tx.add_argument("-a", "--address", type=str, required=True, help="The Ethereum address to query.")
    parser_tx.add_argument("--start_block", type=int, default=0, help="Starting block number.")
    parser_tx.add_argument("--end_block", type=int, default=99999999, help="Ending block number (default latest).")
    parser_tx.add_argument("--page", type=int, default=1, help="Page number for pagination.")
    parser_tx.add_argument("--offset", type=int, default=100, help="Number of transactions per page (max 10000).")
    parser_tx.add_argument("--sort", type=str, default="asc", choices=["asc", "desc"], help="Sort order for transactions.")

    # Subparser for fetching token holders
    parser_holders = subparsers.add_parser("fetch_token_holders", help="Fetch ERC20 token holder list for a contract address.")
    parser_holders.add_argument("-c", "--contract_address", type=str, required=True, help="The ERC20 token contract address.")
    parser_holders.add_argument("--page", type=int, default=1, help="Page number for pagination.")
    parser_holders.add_argument("--offset", type=int, default=100, help="Number of records per page.")

    args = parser.parse_args()
    
    current_api_key = get_api_key(args.api_key)

    if args.action == "fetch_transactions":
        fetch_etherscan_address_transactions(args.address, args.output_file, current_api_key, args.start_block, args.end_block, args.page, args.offset, args.sort)
    elif args.action == "fetch_token_holders":
        fetch_erc20_token_holders(args.contract_address, args.output_file, current_api_key, args.page, args.offset)

