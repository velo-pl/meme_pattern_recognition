# Model Refinement and Expansion Plan

This document outlines the next steps for refining existing AI/ML models and exploring the expansion of our analytical capabilities, following the user's directive to focus on "Further Model Refinement and Expansion".

## 1. Review of Current Models and Capabilities

We have successfully implemented and tested initial versions of:
*   **`sentiment_analyzer.py`**: Currently uses `distilbert-base-uncased-finetuned-sst-2-english` for general sentiment analysis on Twitter and scraped website text.
*   **`onchain_anomaly_detector.py`**: Performs basic rule-based anomaly detection on aggregated Etherscan transaction features for a given dataset.
*   **`risk_flagger.py`**: Identifies predefined risk flags based on scraped website content (team anonymity, whitepaper, roadmap).

These provide a solid foundation. The following sections detail specific areas for refinement and expansion.

## 2. Refinement Opportunities for Existing Models

### 2.1. Sentiment Analyzer (`sentiment_analyzer.py`)

*   **Objective:** Enhance accuracy, provide comparative baselines, and potentially add more nuanced text understanding.
*   **Proposed Refinements:**
    1.  **Domain-Specific Model for Twitter:** Implement and integrate `cardiffnlp/twitter-roberta-base-sentiment-latest`. This model is specifically trained on Twitter data and is likely to yield more accurate results for tweets.
    2.  **Baseline Model (VADER):** Implement VADER (Valence Aware Dictionary and sEntiment Reasoner) as a simpler, rule-based baseline. This will help in evaluating the performance and necessity of more complex transformer models for certain types of text.
    3.  **Model Selection Capability:** Modify the script to allow selection of the sentiment model (e.g., DistilBERT, Twitter-RoBERTa, VADER) via a command-line argument. This will facilitate easier comparison and use.
    4.  **(Future) Emotion Detection:** Explore adding emotion detection (e.g., joy, anger, fear, surprise) as an additional layer to sentiment analysis. This can provide deeper insights into the nuances of community discussions.

### 2.2. On-Chain Anomaly Detector (`onchain_anomaly_detector.py`)

*   **Objective:** Move from basic dataset-wide aggregation to more robust time-series based anomaly detection and expand feature engineering.
*   **Proposed Refinements:**
    1.  **Time-Series Baselining:** Implement true time-series anomaly detection. This involves:
        *   Calculating features (transaction count, volume, etc.) over rolling time windows (e.g., hourly, daily).
        *   Establishing historical baselines (e.g., moving averages, standard deviations) for these features for each specific address being analyzed.
        *   Comparing current window statistics against these historical baselines to identify significant deviations.
    2.  **Advanced Statistical Methods:** Incorporate more advanced statistical methods for outlier detection on the engineered time-series features (e.g., Z-score, Interquartile Range (IQR)).
    3.  **Expanded Feature Engineering:** Introduce new features such as:
        *   Average and standard deviation of time intervals between transactions.
        *   Ratio-based features (e.g., incoming vs. outgoing volume/count within a window).
        *   Interaction with known exchange wallets or flagged suspicious addresses (requires maintaining lists of such addresses).
    4.  **(Future) Clustering for Activity Profiling:** Explore clustering techniques (e.g., K-means, DBSCAN) on transaction features to identify distinct types of on-chain activity and flag unusual or rare clusters.

### 2.3. Risk Flagger (`risk_flagger.py`)

*   **Objective:** Enhance the comprehensiveness and accuracy of risk identification by integrating more data sources and developing a more nuanced scoring system.
*   **Proposed Refinements:**
    1.  **Integration of Other Model Outputs:** Incorporate outputs from the sentiment analyzer and on-chain anomaly detector. For example:
        *   Persistently negative sentiment (from `sentiment_analyzer.py`) could trigger a risk flag.
        *   Frequent or severe on-chain anomalies (from `onchain_anomaly_detector.py`) could contribute to a higher risk assessment.
    2.  **Expanded Data Sources for Risk Flagging:**
        *   **Token Holder Concentration:** This is a high-priority addition. It requires:
            *   Expanding `etherscan_data_collector.py` to fetch top token holder data for specific ERC20 token contracts (e.g., using Etherscan API endpoints like `get_token_info` and `get_token_top_holders`).
            *   Adding logic to `risk_flagger.py` to analyze this data (e.g., flag if top N wallets hold > X% of supply).
        *   **(Future) Social Media Engagement Metrics:** Analyze Twitter user profile data (follower counts vs. engagement on tweets) to flag potential bot activity or inflated community size.
    3.  **(Future) Weighted Risk Scoring:** Transition from binary flags to a weighted risk scoring system. Different identified risks could contribute differently to an overall project risk score, providing a more granular assessment.

## 3. New Model Targets for Expansion

Based on the `pattern_recognition_prioritization.md` and the goal of expanding analytical capabilities:

### 3.1. Topic Modeling
*   **Objective:** To automatically identify and track the main themes and topics of discussion within community forums or social media related to a specific meme coin.
*   **Data Sources:** Cleaned Twitter data, cleaned text from `web_scraper_fundamentals.py` (if it includes forum posts or news articles).
*   **Initial Approach:** Implement topic modeling using techniques such as Latent Dirichlet Allocation (LDA) or Non-negative Matrix Factorization (NMF). Transformer-based approaches like BERTopic can be explored for higher accuracy if resources permit.
*   **Potential Impact:** Understanding what the community is talking about, identifying FUD (Fear, Uncertainty, Doubt) campaigns, or spotting emerging narratives.

## 4. Prioritized Next Steps for Implementation (Phase: Model Refinement & Expansion)

Given the above, the following are proposed as the immediate next steps:

1.  **Sentiment Analyzer Enhancement:**
    *   Integrate `cardiffnlp/twitter-roberta-base-sentiment-latest` into `sentiment_analyzer.py`.
    *   Add VADER as a baseline option.
    *   Update the script to allow model selection via CLI argument.
2.  **On-Chain Anomaly Detector - Time-Series Baselining:**
    *   Modify `onchain_anomaly_detector.py` to implement feature calculation over rolling time windows.
    *   Implement logic to establish and compare against historical baselines for a given address (this will require a strategy for storing/retrieving historical feature data for an address, or processing a longer history file).
3.  **Risk Flagger - Token Holder Concentration (Data Collection First):**
    *   Enhance `etherscan_data_collector.py` to add functionality for fetching top token holder information for specified ERC20 token contract addresses.
    *   Once data collection is possible, update `risk_flagger.py` to include rules for token concentration.

These steps offer a balance of refining existing models for better accuracy and relevance, and laying the groundwork for more sophisticated analysis by expanding data inputs for risk assessment. Topic modeling can be a subsequent step after these refinements are underway.

