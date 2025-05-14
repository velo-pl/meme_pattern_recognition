#!/usr/bin/env python3.11
import requests
from bs4 import BeautifulSoup
import json
import argparse
import re

def fetch_website_text_content(url: str, output_file: str):
    """
    Fetches the main textual content from a given URL and saves it to a JSON file.
    This is a basic scraper and might need adjustments for specific site structures.

    Args:
        url: The URL of the website to scrape.
        output_file: The path to the JSON file where results will be saved.
    """
    print(f"Attempting to scrape content from: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = "\n".join(chunk for chunk in chunks if chunk)
        
        # Try to extract a title if possible
        title_tag = soup.find("title")
        title = title_tag.string.strip() if title_tag else "N/A"

        if cleaned_text:
            print(f"Successfully scraped text content from: {url}")
            data_to_save = {
                "url": url,
                "title": title,
                "scraped_text_content": cleaned_text
            }
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            print(f"Scraped data saved to {output_file}")
        else:
            print(f"No significant text content found at: {url}")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"error": "No significant text content found", "url": url}, f, ensure_ascii=False, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching URL {url}: {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "url": url}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"An unexpected error occurred while processing {url}: {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"error": f"Unexpected error: {str(e)}", "url": url}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch textual content from a website.")
    parser.add_argument("-u", "--url", type=str, required=True, help="The URL of the website to scrape.")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="The path to the output JSON file.")

    args = parser.parse_args()
    fetch_website_text_content(args.url, args.output_file)

