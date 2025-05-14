#!/usr/bin/env python3.11
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
import json
import argparse

def fetch_yahoo_finance_holders_data(symbol: str, output_file: str, region: str = "US", lang: str = "en-US"):
    """
    Fetches stock holder data (insider transactions) from Yahoo Finance API and saves it to a JSON file.

    Args:
        symbol: The stock symbol (e.g., AAPL, MSFT).
        output_file: Path to the output JSON file.
        region: The region for the stock symbol (default US).
        lang: Language for the data (default en-US).
    """
    client = ApiClient()
    print(f"Fetching Yahoo Finance holder data for symbol: {symbol}")
    try:
        params = {
            "symbol": symbol,
            "region": region,
            "lang": lang
        }
        
        response = client.call_api(
            "YahooFinance/get_stock_holders",
            query=params
        )

        if response:
            print(f"Successfully fetched holder data for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
            print(f"Yahoo Finance holder data saved to {output_file}")
        else:
            print(f"No holder data returned from Yahoo Finance API for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "No data returned", "symbol": symbol}, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred while fetching Yahoo Finance holder data for symbol \'{symbol}\': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "symbol": symbol}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock holder data from Yahoo Finance.")
    parser.add_argument("-s", "--symbol", type=str, required=True, help="Stock symbol (e.g., AAPL)." )
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file.")
    parser.add_argument("--region", type=str, default="US", choices=["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "IT", "ES", "GB", "SG"], help="Region for the stock symbol.")
    parser.add_argument("--lang", type=str, default="en-US", choices=["en-US", "pt-BR", "en-AU", "en-CA", "fr-FR", "de-DE", "zh-Hant-HK", "en-IN", "it-IT", "es-ES", "en-GB", "en-SG"], help="Language for the data.")
    
    args = parser.parse_args()
    fetch_yahoo_finance_holders_data(args.symbol, args.output_file, args.region, args.lang)

