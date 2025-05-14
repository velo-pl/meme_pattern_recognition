# AI/ML Model Integration Workflow

This document outlines the workflow for integrating the data collection, cleaning, and analysis scripts to form a cohesive data processing pipeline for the Meme Coin Pattern Recognition Platform.

## 1. Overview

The pipeline consists of the following main stages:
1.  **Data Collection:** Fetching raw data from various sources (Twitter, Yahoo Finance, Etherscan, Websites).
2.  **Data Cleaning:** Processing the raw data to clean, normalize, and prepare it for analysis.
3.  **Data Analysis & Modeling:** Applying specific AI/ML models and analytical scripts to the cleaned data to extract insights (Sentiment Analysis, On-Chain Anomaly Detection, Risk Flagging).

## 2. Core Scripts Involved

*   **Data Collectors:**
    *   `twitter_data_collector.py`
    *   `yahoo_finance_chart_collector.py`
    *   `yahoo_finance_holders_collector.py`
    *   `yahoo_finance_insights_collector.py`
    *   `yahoo_finance_sec_filings_collector.py`
    *   `etherscan_data_collector.py`
    *   `web_scraper_fundamentals.py`
*   **Data Cleaning:**
    *   `data_cleaning_processor.py`
*   **Analysis & Modeling Scripts:**
    *   `sentiment_analyzer.py`
    *   `onchain_anomaly_detector.py`
    *   `risk_flagger.py`

## 3. Integration Workflow and Data Flow

The general workflow for processing a specific type of data (e.g., Twitter data for a particular coin/search query) would be:

**Step A: Data Collection**
*   Run the appropriate data collector script.
    *   Example: `python3.11 /home/ubuntu/project_document/twitter_data_collector.py -q "#SomeCoin" -o /home/ubuntu/raw_data/somecoin_twitter_raw.json -c 100`
*   Output: Raw JSON data file (e.g., `/home/ubuntu/raw_data/somecoin_twitter_raw.json`).

**Step B: Data Cleaning**
*   Run the `data_cleaning_processor.py` script, specifying the input raw data file and the data type.
    *   Example: `python3.11 /home/ubuntu/project_document/data_cleaning_processor.py -i /home/ubuntu/raw_data/somecoin_twitter_raw.json -o /home/ubuntu/cleaned_data/somecoin_twitter_cleaned.json -t twitter`
*   Output: Cleaned JSON data file (e.g., `/home/ubuntu/cleaned_data/somecoin_twitter_cleaned.json`).

**Step C: Data Analysis / Modeling**
*   Run the relevant analysis script, using the cleaned data file as input.

    *   **For Sentiment Analysis (Twitter or Scraped Website Data):**
        *   Input: Cleaned Twitter data or Cleaned Scraped Website data.
        *   Example (Twitter): `python3.11 /home/ubuntu/project_document/sentiment_analyzer.py -i /home/ubuntu/cleaned_data/somecoin_twitter_cleaned.json -o /home/ubuntu/analysis_results/somecoin_twitter_sentiment.json -t twitter`
        *   Example (Website): `python3.11 /home/ubuntu/project_document/sentiment_analyzer.py -i /home/ubuntu/cleaned_data/somecoin_website_cleaned.json -o /home/ubuntu/analysis_results/somecoin_website_sentiment.json -t scraped_website`
        *   Output: JSON file with original data augmented with sentiment scores.

    *   **For On-Chain Anomaly Detection (Etherscan Data):**
        *   Input: Cleaned Etherscan transaction data for a specific address.
        *   Example: `python3.11 /home/ubuntu/project_document/onchain_anomaly_detector.py -i /home/ubuntu/cleaned_data/someaddress_etherscan_cleaned.json -o /home/ubuntu/analysis_results/someaddress_onchain_anomalies.json -a "0xSomeAddress"`
        *   Output: JSON file with calculated features and detected anomalies for the address.

    *   **For Risk Flagging (Primarily Scraped Website Data, potentially others later):**
        *   Input: Cleaned scraped website data for a project.
        *   Example: `python3.11 /home/ubuntu/project_document/risk_flagger.py -i /home/ubuntu/cleaned_data/somecoin_website_cleaned.json -o /home/ubuntu/analysis_results/somecoin_risk_flags.json --project_id "SomeCoinProject"`
        *   Output: JSON file with identified risk flags for the project.

## 4. Directory Structure (Recommended)

To keep data organized, the following directory structure is recommended within `/home/ubuntu/project_data/` (or similar base path):

```
/home/ubuntu/project_data/
├── raw_data/                 # Output from collector scripts
│   ├── somecoin_twitter_raw.json
│   └── someaddress_etherscan_raw.json
├── cleaned_data/             # Output from data_cleaning_processor.py
│   ├── somecoin_twitter_cleaned.json
│   └── someaddress_etherscan_cleaned.json
└── analysis_results/         # Output from analysis/modeling scripts
    ├── somecoin_twitter_sentiment.json
    └── someaddress_onchain_anomalies.json
```
Scripts themselves reside in `/home/ubuntu/project_document/`.

## 5. Considerations for Full Pipeline Automation

*   **Master Script/Orchestrator:** For full automation, a master script (e.g., a Python script using `subprocess` or a shell script) could be developed to run these steps in sequence for multiple coins/projects.
*   **Parameterization:** The master script would need to manage parameters (coin names, addresses, search queries) for each step.
*   **Error Handling:** Robust error handling across the pipeline is crucial.
*   **Data Aggregation for Risk Flagger:** The `risk_flagger.py` currently expects primarily website data. A more advanced version would require an aggregation step where cleaned data from multiple sources (website, on-chain summary, sentiment summary) for a single project is combined into one input file or data structure before being passed to the risk flagger.
*   **Database Integration:** Ultimately, cleaned data and analysis results should be stored in the PostgreSQL database defined in the project plan. This would involve modifying scripts to write to/read from the database instead of just JSON files for persistent storage and more complex querying.

## 6. Next Steps in Integration

1.  **Verify Script Compatibility:** Manually run the sequence for a few sample data types to ensure the output of one script is correctly consumed by the next.
2.  **Create Sample Data and Test Runs:** Prepare small, representative sample raw JSON files for each data type.
3.  **Document Command Examples:** Refine the example commands above with actual file paths and parameters used during testing.
4.  **Develop a Simple Orchestration Example (Optional for now):** A basic shell script demonstrating the chaining for one full data type processing.

This workflow provides a clear path for processing data from collection to analysis. The next phase will involve testing this integrated flow and refining the individual scripts and their interactions.
