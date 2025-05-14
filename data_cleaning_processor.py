#!/usr/bin/env python3.11
import json
import argparse
import pandas as pd
import re
from typing import List, Dict, Any

# Basic text cleaning functions (can be expanded)
def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text) # Replace multiple spaces with single
    text = re.sub(r"[^a-z0-9\s.,!?-]", "", text) # Remove special characters except some punctuation
    return text.strip()

def clean_twitter_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Cleans a list of tweet objects."""
    cleaned_data = []
    seen_ids = set()
    for record in data:
        if not isinstance(record, dict) or "id_str" not in record or not record["id_str"]:
            # Skip malformed records or those without an ID
            continue
        if record["id_str"] in seen_ids:
            continue # Skip duplicates
        seen_ids.add(record["id_str"])

        # Normalize text fields
        if "full_text" in record:
            record["cleaned_full_text"] = normalize_text(record["full_text"])
        if "text" in record: # Older tweet objects might just have text
             record["cleaned_text"] = normalize_text(record["text"])
        
        # Example: Convert created_at to a standard format if needed (assuming it exists)
        # For now, we keep it as is, but this is where date parsing would go.
        cleaned_data.append(record)
    return cleaned_data

def clean_financial_data(data: List[Dict[str, Any]], id_key: str = "symbol") -> List[Dict[str, Any]]:
    """Cleans a list of financial data records (e.g., Yahoo Finance)."""
    # For financial data, we might convert strings to numbers, handle NaNs
    # This is a placeholder; specific cleaning depends on the exact structure
    df = pd.DataFrame(data)
    if df.empty:
        return []
        
    # Drop duplicates based on a unique key if available, or all columns
    if id_key in df.columns:
        df.drop_duplicates(subset=[id_key], keep="first", inplace=True)
    else:
        df.drop_duplicates(keep="first", inplace=True)

    # Example: Convert relevant columns to numeric, coercing errors to NaN
    # for col in ["open", "high", "low", "close", "volume"]:
    #     if col in df.columns:
    #         df[col] = pd.to_numeric(df[col], errors=	"coerce")
    # df.fillna({"volume": 0}, inplace=True) # Fill NaN volumes with 0, other NaNs might be kept or imputed
    
    return df.to_dict(orient="records")

def clean_etherscan_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Cleans a list of Etherscan transaction records."""
    cleaned_data = []
    seen_hashes = set()
    for tx in data:
        if not isinstance(tx, dict) or "hash" not in tx or not tx["hash"]:
            continue
        if tx["hash"] in seen_hashes:
            continue
        seen_hashes.add(tx["hash"])
        
        # Convert relevant string numbers to actual numbers (e.g., value, gasPrice, gasUsed)
        for key in ["value", "gasPrice", "gasUsed", "blockNumber", "timeStamp", "nonce", "transactionIndex", "gas", "cumulativeGasUsed"]:
            if key in tx and isinstance(tx[key], str):
                try:
                    tx[key] = int(tx[key]) if tx[key].isdigit() else float(tx[key])
                except ValueError:
                    pass # Keep as string if conversion fails
        cleaned_data.append(tx)
    return cleaned_data

def clean_scraped_website_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Cleans a single scraped website data object."""
    if not isinstance(data, dict) or "scraped_text_content" not in data:
        return {"error": "Malformed scraped data"}
    
    data["cleaned_scraped_text_content"] = normalize_text(data["scraped_text_content"])
    if "title" in data:
        data["cleaned_title"] = normalize_text(data["title"])
    return data

def main():
    parser = argparse.ArgumentParser(description="Clean and preprocess data from various sources.")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output cleaned JSON file.")
    parser.add_argument("-t", "--data_type", type=str, required=True, 
                        choices=["twitter", "yahoo_finance_chart", "yahoo_finance_holders", 
                                 "yahoo_finance_insights", "yahoo_finance_sec", "etherscan_transactions", "scraped_website"],
                        help="Type of data to clean (e.g., twitter, financial, etherscan, scraped_website).")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from input file: {args.input_file}")
        return

    cleaned_data = None
    if not raw_data and args.data_type not in ["scraped_website"]:
        print(f"Input file {args.input_file} is empty or contains no data. Writing empty list/dict to output.")
        cleaned_data = [] if isinstance(raw_data, list) else {}
    elif args.data_type == "twitter":
        cleaned_data = clean_twitter_data(raw_data if isinstance(raw_data, list) else [])
    elif args.data_type.startswith("yahoo_finance"):
        # Assuming Yahoo finance data is a list of records, or a dict that might contain a list
        # This part might need refinement based on actual API output structure
        data_list = []
        if isinstance(raw_data, list):
            data_list = raw_data
        elif isinstance(raw_data, dict) and "result" in raw_data and isinstance(raw_data["result"], list):
            data_list = raw_data["result"]
        elif isinstance(raw_data, dict) and "chart" in raw_data and isinstance(raw_data["chart"], dict) and "result" in raw_data["chart"] and isinstance(raw_data["chart"]["result"], list):
             data_list = raw_data["chart"]["result"]
        # Add more specific parsing for different yahoo finance endpoints if necessary
        cleaned_data = clean_financial_data(data_list)
    elif args.data_type == "etherscan_transactions":
        cleaned_data = clean_etherscan_transactions(raw_data if isinstance(raw_data, list) else [])
    elif args.data_type == "scraped_website":
        cleaned_data = clean_scraped_website_data(raw_data if isinstance(raw_data, dict) else {})
    else:
        print(f"Error: Unknown data type 	'{args.data_type}	'. No cleaning performed.")
        cleaned_data = raw_data # Pass through if unknown

    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        print(f"Cleaned data saved to {args.output_file}")
    except Exception as e:
        print(f"Error writing cleaned data to {args.output_file}: {e}")

if __name__ == "__main__":
    main()

