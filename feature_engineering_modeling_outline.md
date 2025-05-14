# AI/ML Feature Engineering and Modeling: Outline and Next Steps

This document details the planned approach for feature engineering and the initial development of the prioritized pattern recognition models. It builds upon the `pattern_recognition_prioritization.md` and assumes data has been collected and processed by the scripts outlined in `data_harvesting_gap_analysis.md` and the newly developed collectors and `data_cleaning_processor.py`.

## 1. Introduction

The purpose of this document is to outline the concrete steps for:
1.  Engineering relevant features from our cleaned data sources.
2.  Developing initial versions of the prioritized AI/ML models: Sentiment Analysis, On-Chain Anomaly Detection, and Basic Risk Flag Identification.

This will set the stage for iterative model improvement and the development of more complex analytical capabilities.

## 2. General Prerequisites and Setup

*   **Environment:** Ensure the Python environment has all necessary libraries installed. This includes:
    *   `pandas` and `numpy` for data manipulation.
    *   `scikit-learn` for general machine learning tasks and metrics.
    *   `transformers` (Hugging Face) for pre-trained NLP models.
    *   `nltk` and `spacy` (optional, for more advanced text preprocessing if needed).
    *   `etherscan-python` (already installed for data collection).
    *   `requests` and `beautifulsoup4` (already installed for data collection).
*   **Data Loading Workflow:** Establish a clear Python-based workflow to load the cleaned JSON data outputs from `data_cleaning_processor.py` for each data source type.
*   **Modular Script Development:** Each model or major feature engineering task will be developed in its own Python script (e.g., `sentiment_analyzer.py`, `onchain_feature_extractor.py`, `risk_flagger.py`).

## 3. Model 1: Sentiment Analysis (NLP)

*   **Objective:** To automatically assess and score the sentiment expressed in Twitter data and scraped website text related to meme coins.
*   **Data Sources (Cleaned):**
    *   Twitter data (specifically `cleaned_full_text` or `cleaned_text` fields).
    *   Scraped website content (specifically `cleaned_scraped_text_content` and `cleaned_title` fields).
*   **Feature Engineering Plan:**
    1.  **Text Selection:** Isolate the relevant text fields from the loaded JSON data.
    2.  **Sentiment Scoring:**
        *   **Tool Selection:** Utilize a pre-trained model from the Hugging Face `transformers` library. A good starting point could be `cardiffnlp/twitter-roberta-base-sentiment-latest` for Twitter data due to its training on relevant domain, or a more general model like `distilbert-base-uncased-finetuned-sst-2-english` for broader text. VADER (Valence Aware Dictionary and sEntiment Reasoner) can also be used as a simpler, rule-based baseline, especially for social media text.
        *   **Implementation:** Write a function that takes text as input and returns a sentiment label (positive, negative, neutral) and/or a numerical score (e.g., -1 to 1, or probabilities for each class).
    3.  **Feature Output:** The engineered feature will be the sentiment score/label. This should be appended back to the original data records or stored in a way that it can be easily joined (e.g., by tweet ID or URL).
*   **Initial Modeling Script (`sentiment_analyzer.py`):
    1.  **Functionality:**
        *   Load cleaned text data (from Twitter JSONs, scraped website JSONs).
        *   Initialize the chosen pre-trained sentiment model.
        *   Iterate through text entries, apply sentiment analysis, and store the results.
        *   Save the augmented data (original data + sentiment scores) to a new JSON file.
    2.  **Testing:** Test with sample tweet data and sample scraped website content to ensure scores are generated and correctly appended.

## 4. Model 2: On-Chain Anomaly Detection

*   **Objective:** To identify unusual or potentially suspicious patterns in Ethereum transaction data for specific addresses.
*   **Data Sources (Cleaned):**
    *   Etherscan transaction data (normal transactions for an address).
*   **Feature Engineering Plan (`onchain_feature_extractor.py` or integrated into detector):
    1.  **Data Aggregation:** Group transactions by address and then by time windows (e.g., hourly, daily).
    2.  **Transactional Features (per address, per time window):**
        *   `transaction_count`: Number of transactions.
        *   `total_eth_volume_in/out`: Sum of ETH value for incoming/outgoing transactions.
        *   `avg_eth_transaction_value_in/out`: Average ETH value.
        *   `unique_counterparty_count_in/out`: Number of unique addresses transacted with.
        *   `gas_spent_total/avg`: Total and average gas spent.
        *   `transaction_interval_avg/stddev`: Average and standard deviation of time between transactions.
        *   (Future) Token transfer features if analyzing token contract interactions (would require `get_erc20_token_transfer_events_by_address`).
    3.  **Baseline Calculation:** For each feature, establish a baseline or normal range. This could be a moving average and standard deviation over a longer historical period for the specific address.
*   **Initial Modeling Script (`onchain_anomaly_detector.py`):
    1.  **Functionality:**
        *   Load cleaned Etherscan transaction data for a target address.
        *   Perform feature engineering as outlined above.
        *   **Anomaly Detection Logic (Rule-Based/Statistical):**
            *   For each engineered feature in a given time window, compare it against its historical baseline (e.g., if `transaction_count_daily` > baseline_avg + N * baseline_stddev, flag as anomaly).
            *   Identify sudden large transfers or changes in transaction frequency.
        *   Output a report or augmented data indicating potential anomalies, the features involved, and the time of occurrence.
    2.  **Testing:** Test with transaction data from a known active address and try to manually identify periods that should be flagged.

## 5. Model 3: Basic Risk Flag Identification

*   **Objective:** To implement a rule-based system to identify and flag predefined risks associated with a meme coin project.
*   **Data Sources (Cleaned):**
    *   Scraped website content (for team info, whitepaper presence).
    *   Etherscan data (for token holder concentration if analyzing a token contract - requires `get_token_info` and `get_token_top_holders` or similar, which are beyond current `etherscan_data_collector.py` scope but can be planned).
    *   Yahoo Finance data (e.g., for holder information of related public companies, if any).
*   **Feature Engineering Plan (Data Point Extraction for Rules):
    1.  **Team Anonymity:** From `cleaned_scraped_text_content`, search for keywords like "anonymous team", "team unknown", or absence of a dedicated "Team" section. Output: Boolean flag.
    2.  **Whitepaper Availability:** From `cleaned_scraped_text_content`, search for links containing "whitepaper" or mentions of it. Output: Boolean flag.
    3.  **Token Holder Concentration (Future Enhancement for Token Contracts):** If analyzing a specific token contract, this would involve fetching top holder data and calculating if top N wallets hold > X% of supply. Output: Boolean flag, concentration percentage.
    4.  **Social Media Red Flags (Future Enhancement):** E.g., very low engagement despite high follower count (requires Twitter user profile data beyond basic tweet search).
*   **Initial Modeling Script (`risk_flagger.py`):
    1.  **Functionality:**
        *   Load relevant cleaned data for a project (e.g., scraped website content for a coin's official site).
        *   Implement a series of `if-then` rules based on the extracted data points.
        *   Compile a list of triggered risk flags for the project.
        *   Save the list of flags associated with the project identifier to a JSON file.
    2.  **Testing:** Create mock project data (JSON files) representing different risk profiles and verify that the script correctly identifies the intended flags.

## 6. Next Steps - Implementation and Iteration

1.  **Develop Initial Scripts:** Begin coding `sentiment_analyzer.py`, `onchain_feature_extractor.py` (or integrate into `onchain_anomaly_detector.py`), and `risk_flagger.py`.
2.  **Data Integration for Models:** Ensure these scripts can seamlessly load and process data from the outputs of `data_cleaning_processor.py`.
3.  **Iterative Testing:** Test each script with real (sample) and mock data to validate logic and outputs.
4.  **Refinement:** Based on initial results, refine feature definitions, model parameters (for NLP), and rule thresholds.
5.  **Address Remaining Pipeline Gaps:** Concurrently or subsequently, work on:
    *   More targeted web scrapers for specific tokenomics platforms (e.g., CoinGecko, CoinMarketCap if APIs are not used/available for free tier).
    *   Automation/scheduling of data collection and cleaning scripts.
    *   Expanding Etherscan data collection (e.g., token-specific data, internal transactions).

This structured approach will allow us to build foundational analytical capabilities and progressively enhance the sophistication of our pattern recognition platform.
