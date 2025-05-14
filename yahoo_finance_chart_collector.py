#!/usr/bin/env python3.11
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
import json
import argparse

def fetch_yahoo_finance_chart_data(symbol: str, interval: str, data_range: str, output_file: str, region: str = "US", comparisons: str = "", events: str = "div,split", include_pre_post: bool = False, include_adjusted_close: bool = True):
    """
    Fetches stock chart data from Yahoo Finance API and saves it to a JSON file.

    Args:
        symbol: The stock symbol (e.g., AAPL, MSFT, or crypto like BTC-USD).
        interval: Data interval (e.g., 1m, 5m, 1d, 1wk, 1mo).
        data_range: Data range (e.g., 1d, 5d, 1mo, 1y, max).
        output_file: Path to the output JSON file.
        region: The region for the stock symbol (default US).
        comparisons: Comma-separated symbols for comparison (default "").
        events: Comma-separated event types (default "div,split").
        include_pre_post: Include pre/post market data (default False).
        include_adjusted_close: Include adjusted close data (default True).
    """
    client = ApiClient()
    print(f"Fetching Yahoo Finance chart data for symbol: {symbol}")
    try:
        params = {
            "symbol": symbol,
            "interval": interval,
            "range": data_range,
            "region": region,
            "includePrePost": include_pre_post,
            "includeAdjustedClose": include_adjusted_close,
            "events": events
        }
        if comparisons:
            params["comparisons"] = comparisons
        
        # Note: The API docs mention period1 and period2 but also say not to use with range.
        # For simplicity, this script uses the 'range' parameter.

        response = client.call_api(
            "YahooFinance/get_stock_chart",
            query=params
        )

        if response:
            print(f"Successfully fetched chart data for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
            print(f"Yahoo Finance chart data saved to {output_file}")
        else:
            print(f"No data returned from Yahoo Finance API for symbol: {symbol}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "No data returned", "symbol": symbol}, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred while fetching Yahoo Finance chart data for symbol \'{symbol}\': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "symbol": symbol}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock chart data from Yahoo Finance.")
    parser.add_argument("-s", "--symbol", type=str, required=True, help="Stock symbol (e.g., AAPL, BTC-USD)." )
    parser.add_argument("-i", "--interval", type=str, required=True, choices=["1m", "2m", "5m", "15m", "30m", "60m", "1d", "1wk", "1mo"], help="Data interval.")
    parser.add_argument("-r", "--range", type=str, required=True, choices=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], help="Data range.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file.")
    parser.add_argument("--region", type=str, default="US", choices=["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "IT", "ES", "GB", "SG"], help="Region for the stock symbol.")
    parser.add_argument("--comparisons", type=str, default="", help="Comma-separated symbols for comparison.")
    parser.add_argument("--events", type=str, default="div,split", help="Comma-separated event types.")
    parser.add_argument("--include_pre_post", type=bool, default=False, help="Include pre/post market data.")
    parser.add_argument("--include_adjusted_close", type=bool, default=True, help="Include adjusted close data.")
    
    args = parser.parse_args()
    fetch_yahoo_finance_chart_data(args.symbol, args.interval, args.range, args.output_file, args.region, args.comparisons, args.events, args.include_pre_post, args.include_adjusted_close)

