#!/usr/bin/env python3.11
import sys
sys.path.append("/opt/.manus/.sandbox-runtime")
from data_api import ApiClient
import json
import argparse
import os

def fetch_twitter_data_for_query(query: str, output_file: str, count: int = 20, search_type: str = "Top"):
    """
    Fetches tweets matching a single query using the Twitter API and saves them to a JSON file.

    Args:
        query: The search query for Twitter.
        output_file: The path to the JSON file where results will be saved.
        count: The number of tweets to return (default 20).
        search_type: The type of search (Top, Latest, Photos, Videos, People - default Top).
    """
    client = ApiClient()
    print(f"Fetching Twitter data for query: '{query}' with count: {count}, type: {search_type}")
    try:
        twitter_response = client.call_api(
            "Twitter/search_twitter",
            query={"query": query, "count": count, "type": search_type} # Count should be integer as per API doc
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
        return True
    except Exception as e:
        print(f"An error occurred while fetching Twitter data for query '{query}': {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "query": query}, f, ensure_ascii=False, indent=4)
        return False

def batch_fetch_twitter_data(queries: list[str], output_dir: str, count_per_query: int = 20, search_type: str = "Top"):
    """
    Fetches tweets for a list of queries and saves each to a separate JSON file in the output directory.

    Args:
        queries: A list of search queries for Twitter.
        output_dir: The directory where JSON files will be saved.
        count_per_query: The number of tweets to return for each query.
        search_type: The type of search for each query.
    """
    os.makedirs(output_dir, exist_ok=True)
    all_successful = True
    for query in queries:
        # Sanitize query to create a valid filename
        filename_query = "".join(c if c.isalnum() else "_" for c in query)
        if len(filename_query) > 50: # Truncate if too long
            filename_query = filename_query[:50]
        output_file = os.path.join(output_dir, f"twitter_data_{filename_query}.json")
        print(f"Processing query: '{query}' -> {output_file}")
        success = fetch_twitter_data_for_query(query, output_file, count_per_query, search_type)
        if not success:
            all_successful = False
    return all_successful

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Twitter data for given queries.")
    parser.add_argument("-q", "--query", type=str, help="A single search query for Twitter. If --queries_file is used, this is ignored.")
    parser.add_argument("--queries_file", type=str, help="Path to a text file containing multiple queries, one per line.")
    parser.add_argument("-o", "--output", type=str, required=True, help="The path to the output JSON file (for single query) or output directory (for multiple queries).")
    parser.add_argument("-c", "--count", type=int, default=20, help="Number of tweets to return per query.")
    parser.add_argument("-t", "--type", type=str, default="Top", choices=["Top", "Latest", "Photos", "Videos", "People"], help="Type of search.")

    args = parser.parse_args()

    if args.queries_file:
        try:
            with open(args.queries_file, "r", encoding="utf-8") as f:
                queries_list = [line.strip() for line in f if line.strip()]
            if not queries_list:
                print("Error: Queries file is empty or contains no valid queries.")
                sys.exit(1)
            print(f"Loaded {len(queries_list)} queries from {args.queries_file}")
            batch_fetch_twitter_data(queries_list, args.output, args.count, args.type)
        except FileNotFoundError:
            print(f"Error: Queries file not found at {args.queries_file}")
            sys.exit(1)
    elif args.query:
        fetch_twitter_data_for_query(args.query, args.output, args.count, args.type)
    else:
        print("Error: You must provide either a single --query or a --queries_file.")
        parser.print_help()
        sys.exit(1)

