#!/usr/bin/env python3.11
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
import json
import argparse

def fetch_yahoo_finance_insights_data(symbol: str, output_file: str):
    """
    Fetches stock insights data from Yahoo Finance API and saves it to a JSON file.

    Args:
        symbol: The stock symbol (e.g., AAPL, MSFT).
        output_file: Path to the output JSON file.
    """
    client = ApiClient()
    print(f"Fetching Yahoo Finance insights data for symbol: {symbol}")
    try:
        params = {
            "symbol": symbol
        }
        
        response = client.call_api(
            "YahooFinance/get_stock_insights",
            query=params
        )

        if response:
            print(f"Successfully fetched insights data for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
            print(f"Yahoo Finance insights data saved to {output_file}")
        else:
            print(f"No insights data returned from Yahoo Finance API for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "No data returned", "symbol": symbol}, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred while fetching Yahoo Finance insights data for symbol \'{symbol}\': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "symbol": symbol}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock insights data from Yahoo Finance.")
    parser.add_argument("-s", "--symbol", type=str, required=True, help="Stock symbol (e.g., AAPL)." )
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file.")
    
    args = parser.parse_args()
    fetch_yahoo_finance_insights_data(args.symbol, args.output_file)

