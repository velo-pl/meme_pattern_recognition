import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCoinDetailsByIdentifier } from '../services/apiService';

// Helper function to safely access nested properties
const getNestedValue = (obj, path, defaultValue = 'N/A') => {
  const value = path.split('.').reduce((acc, part) => acc && acc[part], obj);
  return value !== undefined && value !== null ? value : defaultValue;
};

const CoinDetailPage = () => {
  const { identifier } = useParams(); // Get coinId (which is user_screen_name or tweet_id)
  const [coinData, setCoinData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!identifier) return;

    const fetchCoinData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await getCoinDetailsByIdentifier(identifier);
        // The backend directly returns the coin object, not nested under 'scores'
        setCoinData(response.data);
      } catch (err) {
        setError(err.response?.data?.error || err.message || 'Failed to fetch coin details');
        setCoinData(null);
      }
      setIsLoading(false);
    };

    fetchCoinData();
  }, [identifier]);

  if (isLoading) return <p>Loading coin details for {identifier}...</p>;
  if (error) return <p>Error fetching coin details: {error}</p>;
  if (!coinData) return <p>No data found for coin {identifier}.</p>;

  // Define a risk level based on the overall score
  const getRiskLevel = (score) => {
    if (score === null || score === undefined) return 'Unknown';
    if (score >= 7) return 'Low';
    if (score >= 4) return 'Medium';
    return 'High';
  };

  const riskLevel = getRiskLevel(getNestedValue(coinData, 'overall_potential_score_0_10', null));

  return (
    <div>
      <h2>{getNestedValue(coinData, 'user_screen_name')} - Details</h2>
      <p><strong>Overall Potential Score:</strong> {getNestedValue(coinData, 'overall_potential_score_0_10', 'N/A')} / 10</p>
      <p><strong>Calculated Risk Level:</strong> {riskLevel}</p>
      <p><strong>Query Term:</strong> {getNestedValue(coinData, 'query_term')}</p>
      <p><strong>Full Text (if available):</strong> {getNestedValue(coinData, 'full_text', 'Not available')}</p>
      
      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
        <h3>Financial Context (at time of data collection)</h3>
        <p>Price at Tweet Time: {getNestedValue(coinData, 'price_at_tweet_time', 'N/A')}</p>
        <p>Volume at Tweet Time: {getNestedValue(coinData, 'volume_at_tweet_time', 'N/A')}</p>
        <p>Market Cap at Tweet Time: {getNestedValue(coinData, 'market_cap_at_tweet_time', 'N/A')}</p>
        <p>SMA 20 Day Feature: {getNestedValue(coinData, 'sma_20_day_feature', 'N/A')}</p>
        <p>SMA 50 Day Feature: {getNestedValue(coinData, 'sma_50_day_feature', 'N/A')}</p>
        <p>Price Anomalies Count: {getNestedValue(coinData, 'price_anomalies_count_feature', 'N/A')}</p>
        <p>Volume Anomalies Count: {getNestedValue(coinData, 'volume_anomalies_count_feature', 'N/A')}</p>
      </div>

      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
        <h3>Sentiment & Social Scores</h3>
        <p>Calculated Sentiment Score (0-10): {getNestedValue(coinData, 'calculated_sentiment_score_0_10', 'N/A')}</p>
        <p>Raw Sentiment Compound Input: {getNestedValue(coinData, 'sentiment_compound_input', 'N/A')}</p>
        <p>Calculated Engagement Score (0-10): {getNestedValue(coinData, 'calculated_engagement_score_0_10', 'N/A')}</p>
        <p>Engagement Metrics Sum: {getNestedValue(coinData, 'engagement_metrics_sum_feature', 'N/A')}</p>
      </div>
      
      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
        <h3>Scoring Breakdown</h3>
        <p>Overall Potential Score: {getNestedValue(coinData, 'overall_potential_score_0_10', 'N/A')}</p>
        <p>Sentiment Score: {getNestedValue(coinData, 'calculated_sentiment_score_0_10', 'N/A')}</p>
        <p>Engagement Score: {getNestedValue(coinData, 'calculated_engagement_score_0_10', 'N/A')}</p>
        <p>Financial Stability Score: {getNestedValue(coinData, 'context_financial_stability_score_0_10', 'N/A')}</p>
        {/* <p>Trend Following Score: {getNestedValue(coinData, 'trend_following_score_0_10', 'N/A')}</p> */}
      </div>

      {/* Sections for data not currently in integrated_scores.csv - marked as placeholder/future */}
      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc', backgroundColor: '#f0f0f0' }}>
        <h3>Tokenomics (Future Enhancement)</h3>
        <p>Data on total supply, distribution, etc., is not yet available in the current dataset.</p>
      </div>

      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc', backgroundColor: '#f0f0f0' }}>
        <h3>Project Fundamentals (Future Enhancement)</h3>
        <p>Information like whitepaper links and team details is not yet available in the current dataset.</p>
      </div>

    </div>
  );
};

export default CoinDetailPage;

