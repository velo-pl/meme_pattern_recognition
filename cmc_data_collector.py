#!/usr/bin/env python3.11
import os
import json
import requests
import argparse
import time

CMC_API_KEY = ""

def get_newly_added_eth_contracts(api_key, limit=100, existing_contracts=None):
    """
    Fetches newly added cryptocurrencies from CoinMarketCap, 
    filters for Ethereum-based tokens, and extracts their contract addresses.
    Skips contracts already in existing_contracts set.
    """
    if existing_contracts is None:
        existing_contracts = set()
    
    contracts = list(existing_contracts) # Start with existing contracts
    
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    # We sort by date_added to get the newest ones. 
    # We fetch a larger number (e.g., 200) to have enough candidates to filter for Ethereum.
    parameters = {
        "start": "1",
        "limit": str(limit), # Number of results to return
        "sort": "date_added",
        "sort_dir": "desc",
        "cryptocurrency_type": "tokens"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    print(f"Fetching up to {limit} newly added tokens from CoinMarketCap...")

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching listings from CoinMarketCap: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return contracts # Return whatever we have so far
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from CoinMarketCap: {e}")
        print(f"Response content: {response.text}")
        return contracts

    if data.get("status") and data["status"].get("error_code") == 0:
        coins = data.get("data", [])
        print(f"Successfully fetched {len(coins)} tokens. Now filtering for Ethereum platform and extracting contract addresses...")
        
        found_count = 0
        for coin in coins:
            if len(contracts) >= 10 + len(existing_contracts): # Aim for 10 *new* contracts
                break

            coin_id = coin.get("id")
            name = coin.get("name")
            symbol = coin.get("symbol")
            platform = coin.get("platform")

            if platform and platform.get("name") == "Ethereum":
                contract_address = platform.get("token_address")
                if contract_address and contract_address not in contracts:
                    print(f"Found Ethereum token: {name} ({symbol}) - Contract: {contract_address}")
                    contracts.append(contract_address)
                    found_count += 1
                elif contract_address in contracts:
                    print(f"Skipping already collected Ethereum token: {name} ({symbol}) - Contract: {contract_address}")
            # Add a small delay to be respectful to the API, even if not strictly rate-limited here
            time.sleep(0.1)
        print(f"Added {found_count} new Ethereum contract addresses.")
    else:
        error_message = data.get("status", {}).get("error_message", "Unknown API error")
        print(f"CoinMarketCap API Error: {error_message}")

    return contracts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch newly added Ethereum token contract addresses from CoinMarketCap.")
    parser.add_argument("--api_key", type=str, required=True, help="CoinMarketCap API Key.")
    parser.add_argument("--output_file", type=str, default="target_ethereum_meme_coins.txt", help="File to save/append contract addresses.")
    parser.add_argument("--min_total_contracts", type=int, default=10, help="Minimum total number of unique contracts to have in the output file.")
    parser.add_argument("--fetch_limit_per_call", type=int, default=200, help="How many new listings to fetch per API call to find ETH contracts.")

    args = parser.parse_args()
    CMC_API_KEY = args.api_key

    existing_contracts_set = set()
    if os.path.exists(args.output_file):
        print(f"Reading existing contracts from {args.output_file}")
        with open(args.output_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("0x") and len(line) == 42:
                    existing_contracts_set.add(line)
        print(f"Found {len(existing_contracts_set)} existing contracts.")

    if len(existing_contracts_set) < args.min_total_contracts:
        print(f"Attempting to fetch more contracts to reach at least {args.min_total_contracts} total.")
        all_found_contracts_list = get_newly_added_eth_contracts(CMC_API_KEY, limit=args.fetch_limit_per_call, existing_contracts=existing_contracts_set)
        
        # Update the set with newly fetched contracts
        newly_added_count = 0
        for contract in all_found_contracts_list:
            if contract not in existing_contracts_set:
                existing_contracts_set.add(contract)
                newly_added_count +=1
        
        if newly_added_count > 0 or not os.path.exists(args.output_file):
            print(f"Writing {len(existing_contracts_set)} total contracts to {args.output_file}")
            with open(args.output_file, "w") as f:
                for contract in sorted(list(existing_contracts_set)):
                    f.write(contract + "\n")
        else:
            print("No new contracts were added to the list.")
    else:
        print(f"Already have {len(existing_contracts_set)} contracts, which meets or exceeds the minimum of {args.min_total_contracts}.")

    print(f"Process finished. Total unique contracts in {args.output_file}: {len(existing_contracts_set)}")

