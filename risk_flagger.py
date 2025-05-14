#!/usr/bin/env python3.11
import json
import argparse
from typing import List, Dict, Any, Optional
import re
from decimal import Decimal, InvalidOperation

def check_team_anonymity(text_content: Optional[str]) -> bool:
    """Checks for indicators of an anonymous team in the text."""
    if not text_content:
        return True # No content to check, assume anonymous for safety
    text_lower = text_content.lower()
    if "anonymous team" in text_lower or "team is anonymous" in text_lower or "team unknown" in text_lower:
        return True
    team_keywords = ["team", "founders", "about us", "who we are", "our members"]
    if not any(keyword in text_lower for keyword in team_keywords):
        pass 
    return False 

def check_whitepaper_availability(text_content: Optional[str], url: Optional[str] = None) -> bool:
    """Checks for mentions or links to a whitepaper."""
    if not text_content:
        return False 
    text_lower = text_content.lower()
    if "whitepaper" in text_lower or "litepaper" in text_lower:
        return True
    if url and ".pdf" in text_lower: 
        return True
    return False

def check_roadmap_clarity(text_content: Optional[str]) -> bool:
    """Checks for mentions of a roadmap. Basic check."""
    if not text_content:
        return False
    if "roadmap" in text_content.lower() or "future plans" in text_content.lower() or "timeline" in text_content.lower():
        return True
    return False

def check_token_holder_concentration(token_holder_data: Optional[List[Dict[str, str]]], token_decimals: int = 18, top_n: int = 10, threshold_percentage: float = 50.0) -> Optional[str]:
    """Analyzes token holder data for concentration.
    Args:
        token_holder_data: A list of dictionaries, where each dict has at least "TokenHolderAddress" and "TokenHolderQuantity".
        token_decimals: The number of decimals the token uses.
        top_n: The number of top holders to consider for concentration.
        threshold_percentage: The concentration percentage that triggers a warning.
    """
    if not token_holder_data:
        return "Token holder data not available or empty."

    # Convert quantities to Decimal and sort by quantity
    holders_with_balances = []
    total_supply_from_holders = Decimal("0")

    for holder in token_holder_data:
        try:
            quantity_str = holder.get("TokenHolderQuantity")
            if quantity_str is None:
                print(f"Warning: Missing TokenHolderQuantity for holder: {holder.get('TokenHolderAddress')}")
                continue
            # Etherscan API returns quantity as a string representing the raw amount (needs division by 10**decimals)
            balance = Decimal(quantity_str) / (Decimal("10") ** token_decimals)
            holders_with_balances.append({"address": holder.get("TokenHolderAddress"), "balance": balance})
            total_supply_from_holders += balance
        except InvalidOperation:
            print(f"Warning: Could not convert TokenHolderQuantity 	'{holder.get('TokenHolderQuantity')}	' to Decimal for holder: {holder.get('TokenHolderAddress')}")
            continue
        except Exception as e:
            print(f"Warning: Error processing holder {holder.get('TokenHolderAddress')}: {e}")
            continue
            
    if not holders_with_balances:
        return "No valid token holder balances could be processed."

    if total_supply_from_holders == Decimal("0"):
        return "Total supply calculated from holder data is zero, cannot assess concentration."

    # Sort by balance in descending order
    sorted_holders = sorted(holders_with_balances, key=lambda x: x["balance"], reverse=True)

    # Calculate concentration for top N holders
    top_n_sum = sum(h["balance"] for h in sorted_holders[:top_n])
    
    if total_supply_from_holders > 0:
        concentration_percentage = (top_n_sum / total_supply_from_holders) * Decimal("100")
    else: # Should be caught by earlier check, but as a safeguard
        concentration_percentage = Decimal("0")

    if concentration_percentage >= Decimal(str(threshold_percentage)):
        return f"High concentration: Top {top_n} holders own {concentration_percentage:.2f}% of the analyzed supply."
    else:
        return f"Concentration check: Top {top_n} holders own {concentration_percentage:.2f}% of the analyzed supply."

def identify_risk_flags(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Identifies risk flags based on various data points for a project."""
    flags = {}
    
    scraped_content_data = project_data.get("scraped_website_content")
    website_text = None
    website_url = None
    if isinstance(scraped_content_data, dict):
        website_text = scraped_content_data.get("cleaned_scraped_text_content")
        website_url = scraped_content_data.get("url")

    flags["team_anonymous_flag"] = check_team_anonymity(website_text)
    flags["whitepaper_missing_flag"] = not check_whitepaper_availability(website_text, website_url)
    flags["roadmap_unclear_flag"] = not check_roadmap_clarity(website_text)

    token_holders_raw = project_data.get("token_holder_data") # Expects list of dicts from Etherscan collector
    # Assuming token_decimals is either passed in project_data or we use a default
    token_decimals_val = project_data.get("token_decimals", 18) 
    flags["token_concentration_analysis"] = check_token_holder_concentration(token_holders_raw, token_decimals_val)
    
    active_flags_summary = []
    for key, value in flags.items():
        if value is True:
            active_flags_summary.append(key)
        elif isinstance(value, str) and ("High concentration:" in value or "Token holder data not available" in value or "No valid token holder balances" in value or "Total supply calculated from holder data is zero" in value) :
             active_flags_summary.append(f"{key}: {value}")
        # Add other conditions for string-based flags if necessary

    if not active_flags_summary:
        active_flags_summary = ["No specific red flags identified based on current rules and available data."]

    return {
        "project_identifier": project_data.get("identifier", "N/A"),
        "detailed_flags": flags,
        "active_flags_summary": active_flags_summary
    }

def main():
    parser = argparse.ArgumentParser(description="Identify risk flags for a project based on aggregated data.")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input JSON file containing aggregated project data (e.g., website scrape, token holders)." )
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file with identified risk flags.")
    parser.add_argument("--project_id", type=str, default="unknown_project", help="An identifier for the project being analyzed.")
    parser.add_argument("--token_decimals", type=int, default=18, help="The number of decimals for the token being analyzed (used for holder concentration).")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            input_data_content = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from input file: {args.input_file}")
        return

    # The input_file is now expected to be a dictionary that might contain
    # 'scraped_website_content' and/or 'token_holder_data' keys.
    project_data_for_flagger = {
        "identifier": args.project_id,
        "scraped_website_content": input_data_content.get("scraped_website_content"),
        "token_holder_data": input_data_content.get("token_holder_data"),
        "token_decimals": args.token_decimals # Pass token decimals from CLI or use default
    }

    print(f"Identifying risk flags for project: {args.project_id} from file: {args.input_file}")
    risk_analysis_results = identify_risk_flags(project_data_for_flagger)

    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(risk_analysis_results, f, ensure_ascii=False, indent=4)
        print(f"Risk flag analysis results saved to {args.output_file}")
    except Exception as e:
        print(f"Error writing risk flag results to {args.output_file}: {e}")

if __name__ == "__main__":
    main()

