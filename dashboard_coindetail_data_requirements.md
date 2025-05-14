## Data Requirements for Dashboard and Coin Detail Pages

This document outlines the data needed to integrate the `DashboardPage.jsx` and `CoinDetailPage.jsx` components with the backend API, moving from placeholder data to dynamic content.

### 1. DashboardPage (`DashboardPage.jsx`)

The dashboard aims to provide a high-level overview of the meme coin market analysis.

**Data Needs:**

*   **Summary Statistics:**
    *   **Total Coins Analyzed:** A count of all unique coins/entities present in the `integrated_scores.csv` dataset.
    *   **Promising Coins Identified (e.g., last 30 days):** A count of coins meeting a defined "promising" threshold (e.g., `overall_potential_score_0_10` >= 8). *Further definition of "promising" and time-windowing logic might be needed.*
    *   **High-Risk Coins Flagged (e.g., last 30 days):** A count of coins meeting a defined "high-risk" threshold (e.g., `overall_potential_score_0_10` <= 3, or a dedicated risk flag). *Further definition of "high-risk" and time-windowing logic might be needed.*

*   **Top Promising Coins:**
    *   A list (e.g., top 3-5) of the most promising coins.
    *   Required fields per coin: `user_screen_name` (or a display name), `overall_potential_score_0_10`.
    *   Data source: `/api/v1/scores`, sorted by `overall_potential_score_0_10` descending.

*   **High-Risk Alerts:**
    *   A list (e.g., top 3-5) of the highest-risk coins.
    *   Required fields per coin: `user_screen_name` (or a display name), `overall_potential_score_0_10` (or a specific risk score/flag).
    *   Data source: `/api/v1/scores`, sorted/filtered by risk criteria.

**API Endpoint Usage:**
*   Primarily use the existing `/api/v1/scores` endpoint. The frontend will perform necessary calculations, sorting, and filtering for the initial implementation.
*   Future enhancements might involve dedicated backend endpoints for aggregated statistics if client-side processing becomes too heavy.

### 2. Coin Detail Page (`CoinDetailPage.jsx`)

The coin detail page aims to provide an in-depth view of a single selected meme coin.

**Data Needs (for a single coin, identified by a unique ID like `user_screen_name` or `tweet_id` from the list page):**

*   **Basic Information:**
    *   `user_screen_name` (Primary Identifier/Display Name)
    *   `tweet_id` (if applicable, or another unique ID)
    *   `query_term` (e.g., "meme coin")
    *   `full_text` (from Twitter data, can serve as a description if relevant)
    *   `overall_potential_score_0_10`
    *   *Risk Level:* This needs to be derived or defined. Could be based on `overall_potential_score_0_10` ranges.

*   **Financials (primarily from Yahoo Finance features in `integrated_scores.csv`):**
    *   `price_at_tweet_time` (if available and relevant, or current price if we add a live feed - current data is point-in-time)
    *   `volume_at_tweet_time`
    *   `market_cap_at_tweet_time`
    *   `sma_20_day_feature`, `sma_50_day_feature`
    *   `price_anomalies_count_feature`, `volume_anomalies_count_feature` (or specific anomaly descriptions if stored)
    *   *Note: The placeholder data includes fields like `price`, `volume24h`, `marketCap` which imply current data. The `integrated_scores.csv` has point-in-time financial context. This discrepancy needs to be addressed in UI presentation or by enhancing data pipelines.*

*   **Sentiment & Social (from Twitter features in `integrated_scores.csv`):**
    *   `calculated_sentiment_score_0_10`
    *   `sentiment_compound_input` (raw compound score)
    *   `engagement_metrics_sum_feature` (or `calculated_engagement_score_0_10`)
    *   *Placeholder data mentions `positiveTweets`, `negativeTweets`, `neutralTweets`, and `recentTweets`. The current `integrated_scores.csv` has aggregated sentiment and engagement scores. Displaying individual tweets or tweet counts would require changes to data storage and API structure.*

*   **Scoring Breakdown:**
    *   `calculated_sentiment_score_0_10`
    *   `calculated_engagement_score_0_10`
    *   `context_financial_stability_score_0_10`
    *   `trend_following_score_0_10` (if this feature is developed and included)

*   **Placeholder Sections (Data currently unavailable in `integrated_scores.csv` - may require new data sources/features):**
    *   Tokenomics (Total Supply, Distribution)
    *   Project Fundamentals (Whitepaper link, Team information)

**API Endpoint Usage:**
*   A new endpoint, e.g., `/api/v1/scores/<identifier>`, will be needed. The `<identifier>` could be `user_screen_name` or another unique key from the `integrated_scores.csv`.
*   This endpoint should fetch the complete record for the specified coin from `integrated_scores.csv`.

### Implementation Notes:
*   The frontend will need routing capabilities (e.g., using React Router) to navigate to `CoinDetailPage` with a specific coin identifier in the URL.
*   The `coinId` in `CoinDetailPage.jsx` (currently placeholder `pepe`) will need to be dynamically obtained from the URL parameters.
*   Error handling for cases where a coin ID is not found or API calls fail is crucial.
*   For data not currently available (e.g., detailed tokenomics, recent individual tweets), these sections should either be omitted, clearly marked as "Data Unavailable," or continue to use illustrative placeholders for the initial integration, with a plan to enhance data sources later.
