## Data Visualization Plan for Meme Coin Platform

This document outlines the proposed data visualizations for the Dashboard and Coin Detail pages of the Meme Coin Pattern Recognition Platform. The goal is to provide users with clear, actionable insights into the analyzed meme coins.

### Data Source

The primary data source for these visualizations will be the `integrated_scores.csv` file, which includes fields such as:
*   `user_screen_name`
*   `overall_potential_score_0_10`
*   `calculated_sentiment_score_0_10`
*   `calculated_engagement_score_0_10`
*   `context_financial_stability_score_0_10`
*   `tweet_id` (can be used as a unique identifier for tweet-based entries)
*   `full_text`

### I. Dashboard Page Visualizations

The Dashboard aims to provide a high-level overview of the meme coin landscape based on the latest analysis.

1.  **Overall Potential Score Distribution (Histogram or Bar Chart):**
    *   **Purpose:** To show the distribution of `overall_potential_score_0_10` across all analyzed coins/tweets.
    *   **Chart Type:** Histogram (if scores are continuous enough) or a Bar Chart with binned score ranges (e.g., 0-2, 2-4, 4-6, 6-8, 8-10).
    *   **X-axis:** Score or Score Range.
    *   **Y-axis:** Number of Coins/Tweets.
    *   **Insights:** Helps understand the general quality/potential of the analyzed set. Are most coins low potential, high potential, or evenly distributed?

2.  **Top N Promising Coins (Horizontal Bar Chart):**
    *   **Purpose:** To highlight the top N (e.g., 5 or 10) coins/tweets with the highest `overall_potential_score_0_10`.
    *   **Chart Type:** Horizontal Bar Chart.
    *   **Y-axis:** `user_screen_name` (or `tweet_id` if more appropriate).
    *   **X-axis:** `overall_potential_score_0_10`.
    *   **Interactivity:** Clicking on a bar could navigate to the `CoinDetailPage` for that specific coin/tweet.
    *   **Insights:** Quickly identifies the most promising opportunities based on the integrated score.

3.  **Sentiment vs. Engagement Overview (Scatter Plot - Optional, if data diversity allows):**
    *   **Purpose:** To visualize the relationship between `calculated_sentiment_score_0_10` and `calculated_engagement_score_0_10` for all coins/tweets.
    *   **Chart Type:** Scatter Plot.
    *   **X-axis:** `calculated_sentiment_score_0_10`.
    *   **Y-axis:** `calculated_engagement_score_0_10`.
    *   **Dot Size/Color (Optional):** Could represent `overall_potential_score_0_10` or `context_financial_stability_score_0_10`.
    *   **Insights:** Helps identify coins that have high sentiment but low engagement, or vice-versa, or those strong in both. This might be more useful with a larger, more diverse dataset.

4.  **Score Component Averages (Grouped Bar Chart or Radar Chart):**
    *   **Purpose:** To show the average of each core score component (`calculated_sentiment_score_0_10`, `calculated_engagement_score_0_10`, `context_financial_stability_score_0_10`) across all analyzed items.
    *   **Chart Type:** Grouped Bar Chart (components on X-axis, average score on Y-axis) or a Radar Chart (each axis representing a score component).
    *   **Insights:** Provides a snapshot of the general strengths and weaknesses of the market or analyzed set according to the scoring model.

### II. Coin Detail Page Visualizations

The Coin Detail Page aims to provide an in-depth look at a single selected meme coin/tweet.

1.  **Individual Score Breakdown (Gauge Charts or Bar Chart):**
    *   **Purpose:** To clearly display the specific scores for the selected coin: `overall_potential_score_0_10`, `calculated_sentiment_score_0_10`, `calculated_engagement_score_0_10`, and `context_financial_stability_score_0_10`.
    *   **Chart Type:** A set of Gauge Charts (one for each score) or a single vertical/horizontal Bar Chart showing these four scores.
    *   **Insights:** Provides an immediate visual understanding of the coin's performance across the key metrics.

2.  **Comparison to Average (Bar Chart - Optional):**
    *   **Purpose:** To compare the selected coin's scores against the average scores of all analyzed coins (from Dashboard visualization 4).
    *   **Chart Type:** Grouped Bar Chart, showing the selected coin's score and the average score for each component side-by-side.
    *   **Insights:** Helps contextualize the individual coin's performance relative to the broader set.

### Implementation Notes
*   **Library:** Recharts will be used for implementing these visualizations in the React frontend.
*   **Data Fetching:** Visualizations will use the data already being fetched and managed by the Zustand store.
*   **Responsiveness:** All charts will be designed to be responsive and display well on different screen sizes.
*   **Tooltips:** Interactive tooltips will be added to charts to show precise values on hover.
*   **Error Handling:** Graceful handling for cases where data might be missing or insufficient for a particular chart.

This plan provides a starting point. The actual implementation may involve adjustments based on data characteristics discovered during development and user feedback.

