# Data Harvesting Gap Analysis and Requirements

This document outlines the identified gaps in the current data harvesting capabilities and the requirements for expanding the data collection pipelines, based on the project's `implementation_plan.md` and `todo.md`.

## 1. Current Data Collection Capabilities

The project currently has Python scripts for collecting data from the following sources using the `ApiClient`:

*   **Twitter:**
    *   `twitter_data_collector.py`: Fetches tweets based on search queries.
*   **Yahoo Finance:**
    *   `yahoo_finance_chart_collector.py`: Fetches stock chart data.
    *   `yahoo_finance_holders_collector.py`: Fetches stock holder data (insider transactions).
    *   `yahoo_finance_insights_collector.py`: Fetches stock insights data.
    *   `yahoo_finance_sec_filings_collector.py`: Fetches company SEC filing history.

These scripts provide a good foundation for social media sentiment and basic financial market data.

## 2. Identified Gaps in Data Sources

Based on the project documentation (`implementation_plan.md`, `data_source_mapping.md`, and `todo.md`), the following data categories and sources are required but currently lack dedicated collection scripts or mechanisms:

*   **On-Chain Data:**
    *   **Requirement:** Transaction volumes, wallet activities, smart contract interactions, token movements, gas fees, etc., for relevant blockchains (e.g., Ethereum, BNB Chain, Solana).
    *   **Gap:** No scripts or API integrations identified for accessing on-chain data. Potential sources include Etherscan API, BscScan API, Glassnode, Nansen, or other blockchain explorers/analytics platforms.
*   **Tokenomics Data:**
    *   **Requirement:** Total supply, circulating supply, token distribution, vesting schedules, inflation/deflation mechanisms, utility of the token within its ecosystem.
    *   **Gap:** No dedicated scripts. Some of this information might be found on project websites, whitepapers, or platforms like CoinGecko/CoinMarketCap, which may require web scraping or dedicated API usage if available.
*   **Project Fundamentals Data:**
    *   **Requirement:** Whitepaper analysis, team background and experience, project roadmap and progress, community engagement levels (beyond Twitter, e.g., Discord, Telegram), audit reports, partnerships.
    *   **Gap:** No dedicated scripts. This data often requires parsing unstructured text from whitepapers (PDFs), project websites (HTML), and community forums. Web scraping and NLP techniques will be essential.
*   **Exchange Listings and Trading Data (Beyond Yahoo Finance for broader crypto coverage):**
    *   **Requirement:** Listing dates on various exchanges, trading pairs, liquidity, order book depth from major cryptocurrency exchanges.
    *   **Gap:** While Yahoo Finance covers some crypto, dedicated crypto exchange APIs (e.g., Binance, Coinbase, Kraken) would provide more comprehensive and real-time trading data. No scripts for these are currently present.
*   **News and Media Mentions (Broader Scope):**
    *   **Requirement:** Mentions in crypto-specific news outlets, financial news sites, and influential blogs.
    *   **Gap:** While Twitter covers social sentiment, a broader news aggregation strategy might be needed. This could involve news APIs (e.g., NewsAPI.org, GNews) or web scraping of specific outlets.

## 3. Gaps in Data Collection Process and Infrastructure

*   **Ethical Web Scrapers:**
    *   **Requirement:** As per `todo.md` (Phase 2.2), development of ethical web scrapers is pending. These will be crucial for tokenomics and project fundamentals data.
    *   **Gap:** No web scraping scripts or framework (e.g., Scrapy, BeautifulSoup with Requests) implementation is evident.
*   **Scheduled Data Collection:**
    *   **Requirement:** As per `todo.md` (Phase 2.2), scheduling data collection (e.g., using cron or a workflow orchestrator like Airflow if feasible) is pending.
    *   **Gap:** Current scripts are manually executed. Automation is needed for continuous data ingestion.
*   **Data Cleaning, Preprocessing, and Validation Scripts:**
    *   **Requirement:** As per `todo.md` (Phase 2.4), scripts for data cleaning, transformation, and validation are pending.
    *   **Gap:** No dedicated scripts for these crucial data quality steps are present. This will be vital before data is used for feature engineering and model training.
*   **Database Population and Management:**
    *   **Requirement:** Robust population of the PostgreSQL database with diverse and clean data. The `todo.md` notes initial population with a single Twitter API error response, indicating a need for actual data loading.
    *   **Gap:** While the schema is designed and the DB is set up, systematic data loading and validation processes from all collected sources into the database are not yet fully implemented.

## 4. Requirements for Next Steps (Expanding Data Pipelines)

1.  **Prioritize Missing Data Sources:** Based on their impact on pattern recognition, prioritize the development of collectors for on-chain data, tokenomics, and project fundamentals.
2.  **Develop Web Scraping Capabilities:** Implement a robust and ethical web scraping framework to gather data from project websites, whitepapers, and other relevant online sources.
3.  **Integrate New APIs:** Identify and integrate APIs for on-chain data (e.g., Etherscan, BscScan), comprehensive crypto exchange data, and potentially broader news aggregation.
4.  **Implement Data Cleaning and Preprocessing:** Develop Python scripts to clean, transform, and validate data from all sources before database insertion. Handle missing values, outliers, and inconsistencies.
5.  **Automate Data Collection:** Implement scheduling mechanisms (e.g., cron jobs in the sandbox) to automate the execution of all data collection and processing scripts.
6.  **Enhance Database Interaction:** Develop scripts for systematically loading processed data into the PostgreSQL database, ensuring data integrity and consistency with the defined schema.
7.  **Error Handling and Logging:** Improve error handling and logging in all data collection scripts to ensure reliability and traceability.

