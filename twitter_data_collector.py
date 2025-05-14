#!/usr/bin/env python3.11
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
import json
import argparse

def fetch_twitter_data(query: str, output_file: str, count: int = 20, search_type: str = "Top"):
    """
    Fetches tweets matching a query using the Twitter API and saves them to a JSON file.
    Hypothesis: The API might expect the 'count' parameter as a string.

    Args:
        query: The search query for Twitter.
        output_file: The path to the JSON file where results will be saved.
        count: The number of tweets to return (default 20).
        search_type: The type of search (Top, Latest, Photos, Videos, People - default Top).
    """
    client = ApiClient()
    print(f"Fetching Twitter data for query: {query} with count as STRING: 	{str(count)}")
    try:
        # MODIFICATION: Pass count as a string
        twitter_response = client.call_api(
            "Twitter/search_twitter",
            query={"query": query, "count": str(count), "type": search_type}
        )

        if twitter_response:
            print(f"Successfully fetched data for query: {query}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(twitter_response, f, ensure_ascii=False, indent=4)
            print(f"Twitter data saved to {output_file}")
        else:
            print(f"No data returned from Twitter API for query: {query}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "No data returned", "query": query}, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred while fetching Twitter data for query 	'{query}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "query": query}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Twitter data for a given query.")
    parser.add_argument("-q", "--query", type=str, required=True, help="The search query for Twitter.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="The path to the output JSON file.")
    parser.add_argument("-c", "--count", type=int, default=20, help="Number of tweets to return.")
    parser.add_argument("-t", "--type", type=str, default="Top", choices=["Top", "Latest", "Photos", "Videos", "People"], help="Type of search.")

    args = parser.parse_args()
    fetch_twitter_data(args.query, args.output_file, args.count, args.type)

