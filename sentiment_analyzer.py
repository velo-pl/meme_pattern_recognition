#!/usr/bin/env python3.11
import json
import argparse
import pandas as pd
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk # NLTK is required for VADER
from typing import List, Dict, Any, Optional

# Global variable for the initialized pipeline or VADER analyzer
ANALYSIS_TOOL = None
CURRENT_MODEL_NAME = None

def download_nltk_resources_if_needed():
    """Downloads NLTK resources required for VADER if not already present."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
        print("VADER lexicon found.")
    except LookupError: # Corrected exception type
        print("VADER lexicon not found. Downloading...")
        nltk.download("vader_lexicon")
        print("VADER lexicon downloaded successfully.")
    except Exception as e:
        print(f"Error checking/downloading VADER lexicon: {e}")

def initialize_analysis_tool(model_name_or_type: str = "distilbert"):
    """Initializes the selected sentiment analysis tool (Hugging Face pipeline or VADER)."""
    global ANALYSIS_TOOL, CURRENT_MODEL_NAME
    
    if ANALYSIS_TOOL is not None and CURRENT_MODEL_NAME == model_name_or_type:
        print(f"Analysis tool ({model_name_or_type}) already initialized.")
        return

    print(f"Initializing sentiment analysis tool: {model_name_or_type}...")
    CURRENT_MODEL_NAME = model_name_or_type
    
    if model_name_or_type.lower() == "vader":
        download_nltk_resources_if_needed()
        try:
            ANALYSIS_TOOL = SentimentIntensityAnalyzer()
            print("VADER sentiment analyzer initialized successfully.")
        except Exception as e:
            print(f"Error initializing VADER: {e}")
            ANALYSIS_TOOL = None
            CURRENT_MODEL_NAME = None
    elif model_name_or_type.lower() == "distilbert":
        hf_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        try:
            ANALYSIS_TOOL = pipeline("sentiment-analysis", model=hf_model_name)
            print(f"Hugging Face pipeline ({hf_model_name}) initialized successfully.")
        except Exception as e:
            print(f"Error initializing Hugging Face pipeline ({hf_model_name}): {e}")
            ANALYSIS_TOOL = None
            CURRENT_MODEL_NAME = None
    elif model_name_or_type.lower() == "twitter-roberta":
        hf_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        try:
            ANALYSIS_TOOL = pipeline("sentiment-analysis", model=hf_model_name)
            print(f"Hugging Face pipeline ({hf_model_name}) initialized successfully.")
        except Exception as e:
            print(f"Error initializing Hugging Face pipeline ({hf_model_name}): {e}")
            ANALYSIS_TOOL = None
            CURRENT_MODEL_NAME = None
    else:
        print(f"Error: Unknown model name or type 	'{model_name_or_type}'. Defaulting to DistilBERT if possible or None.")
        # Attempt to default or handle error
        try:
            ANALYSIS_TOOL = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            CURRENT_MODEL_NAME = "distilbert"
            print("Defaulted to DistilBERT pipeline.")
        except Exception as e:
            print(f"Error initializing default DistilBERT pipeline: {e}")
            ANALYSIS_TOOL = None
            CURRENT_MODEL_NAME = None

def analyze_sentiment_with_tool(text: str) -> Dict[str, Any]:
    """Analyzes the sentiment of a given text string using the initialized tool."""
    if ANALYSIS_TOOL is None:
        return {"error": f"Sentiment analysis tool ({CURRENT_MODEL_NAME or 'Unknown'}) not initialized or failed to initialize."}
    if not isinstance(text, str) or not text.strip():
        return {"label": "NEUTRAL", "score": 0.0, "error": "Empty or invalid text"}

    try:
        if CURRENT_MODEL_NAME == "vader":
            # VADER returns a dict like: {'neg': 0.0, 'neu': 0.326, 'pos': 0.674, 'compound': 0.7717}
            vader_scores = ANALYSIS_TOOL.polarity_scores(text)
            compound_score = vader_scores["compound"]
            if compound_score >= 0.05:
                label = "POSITIVE"
            elif compound_score <= -0.05:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            return {"label": label, "score": compound_score, "vader_scores": vader_scores} # score is compound
        
        elif CURRENT_MODEL_NAME in ["distilbert", "twitter-roberta"]:
            # Hugging Face pipelines return a list of dictionaries, e.g., [{'label': 'POSITIVE', 'score': 0.9998}]
            # Truncate text to avoid issues with model max length. Common models have 512 token limit.
            max_length = 510 # A bit less than 512 to be safe with tokenization
            truncated_text = text[:max_length] if len(text) > max_length else text
            
            result = ANALYSIS_TOOL(truncated_text)
            if result and isinstance(result, list) and len(result) > 0:
                # Normalize RoBERTa labels (LABEL_0, LABEL_1, LABEL_2 to Negative, Neutral, Positive)
                hf_result = result[0]
                if CURRENT_MODEL_NAME == "twitter-roberta":
                    if hf_result["label"] == "LABEL_0":
                        hf_result["label"] = "NEGATIVE"
                    elif hf_result["label"] == "LABEL_1":
                        hf_result["label"] = "NEUTRAL"
                    elif hf_result["label"] == "LABEL_2":
                        hf_result["label"] = "POSITIVE"
                return hf_result
            else:
                return {"label": "NEUTRAL", "score": 0.0, "error": "Sentiment analysis returned no result"}
        else:
            return {"error": f"Analysis logic not implemented for model: {CURRENT_MODEL_NAME}"}
            
    except Exception as e:
        print(f"Error during sentiment analysis for text 	'{text[:50]}...	' with {CURRENT_MODEL_NAME}: {e}")
        return {"label": "ERROR", "score": 0.0, "error": str(e)}

def process_data_for_sentiment(data: List[Dict[str, Any]], text_key: str, id_key: str, model_name_or_type: str) -> List[Dict[str, Any]]:
    """Processes a list of records, adding sentiment analysis results using the specified model."""
    initialize_analysis_tool(model_name_or_type)
    if ANALYSIS_TOOL is None:
        print(f"Skipping sentiment analysis as tool ({model_name_or_type}) failed to initialize.")
        for record in data:
            record[f"sentiment_analysis_{model_name_or_type.replace('-', '_')}"] = {"error": f"Sentiment tool {model_name_or_type} not initialized"}
        return data

    processed_records = []
    for record_idx, record in enumerate(data):
        if not isinstance(record, dict):
            processed_records.append({"original_record_error": "Malformed record", "data": record})
            continue
        
        print(f"Processing record {record_idx + 1}/{len(data)} with {model_name_or_type}...")
        text_to_analyze = record.get(text_key)
        sentiment_result = analyze_sentiment_with_tool(text_to_analyze)
        record[f"sentiment_analysis_{model_name_or_type.replace('-', '_')}"] = sentiment_result
        processed_records.append(record)
    return processed_records

def main():
    parser = argparse.ArgumentParser(description="Perform sentiment analysis on text data from JSON files.")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input JSON file (cleaned data)." )
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file with sentiment scores.")
    parser.add_argument("-t", "--data_type", type=str, required=True, choices=["twitter", "scraped_website"], help="Type of data to process.")
    parser.add_argument("-m", "--model", type=str, default="distilbert", choices=["distilbert", "twitter-roberta", "vader"], help="Sentiment analysis model to use.")
    parser.add_argument("--text_key", type=str, help="The key in the JSON objects that contains the text to analyze. Inferred if not provided.")
    parser.add_argument("--id_key", type=str, help="The key in the JSON objects that serves as a unique identifier. Inferred if not provided.")

    args = parser.parse_args()

    text_key = args.text_key
    id_key = args.id_key
    if not text_key:
        text_key = "cleaned_full_text" if args.data_type == "twitter" else "cleaned_scraped_text_content"
    if not id_key:
        id_key = "id_str" if args.data_type == "twitter" else "url"
            
    if not text_key or not id_key:
        print(f"Error: Could not infer text_key or id_key for data_type 	'{args.data_type}'. Provide via --text_key and --id_key.")
        return

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from input file: {args.input_file}")
        return

    if not isinstance(input_data, list):
        if args.data_type == "scraped_website" and isinstance(input_data, dict):
            input_data = [input_data]
        else:
            print(f"Error: Input data is not a list of records. Found type: {type(input_data)}")
            return

    print(f"Processing {len(input_data)} records from {args.input_file} for sentiment analysis using {args.model} model...")
    output_data = process_data_for_sentiment(input_data, text_key, id_key, args.model)

    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        print(f"Sentiment analysis results using {args.model} saved to {args.output_file}")
    except Exception as e:
        print(f"Error writing sentiment analysis results to {args.output_file}: {e}")

if __name__ == "__main__":
    main()

