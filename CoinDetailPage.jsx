import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCoinDetailsByIdentifier } from '../services/apiService';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

// Helper function to safely access nested properties
const getNestedValue = (obj, path, defaultValue = 'N/A') => {
  const value = path.split('.').reduce((acc, part) => acc && acc[part], obj);
  // Ensure that 0 is a valid value and not treated as 'N/A'
  return value !== undefined && value !== null ? value : defaultValue;
};

const ScoreBarChart = ({ data, title }) => {
  if (!data || data.length === 0) {
    return <p>No data available for {title}.</p>;
  }

  // Define colors for bars - can be expanded or customized
  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#d0ed57', '#a4de6c'];

  return (
    <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 10]} ticks={[0, 2, 4, 6, 8, 10]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="score" fill="#8884d8">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const CoinDetailPage = () => {
  const { identifier } = useParams();
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

  const getRiskLevel = (score) => {
    if (score === null || score === undefined || score === 'N/A') return 'Unknown';
    if (score >= 7) return 'Low';
    if (score >= 4) return 'Medium';
    return 'High';
  };

  const overallScore = getNestedValue(coinData, 'overall_potential_score_0_10', null);
  const riskLevel = getRiskLevel(overallScore);

  const scoreBreakdownData = [
    { name: 'Overall Potential', score: parseFloat(getNestedValue(coinData, 'overall_potential_score_0_10', 0)) },
    { name: 'Sentiment', score: parseFloat(getNestedValue(coinData, 'calculated_sentiment_score_0_10', 0)) },
    { name: 'Engagement', score: parseFloat(getNestedValue(coinData, 'calculated_engagement_score_0_10', 0)) },
    { name: 'Financial Stability', score: parseFloat(getNestedValue(coinData, 'context_financial_stability_score_0_10', 0)) },
  ].filter(item => item.score !== 'N/A' && !isNaN(item.score));

  return (
    <div>
      <h2>{getNestedValue(coinData, 'user_screen_name')} - Details</h2>
      <p><strong>Overall Potential Score:</strong> {overallScore === null ? 'N/A' : overallScore} / 10</p>
      <p><strong>Calculated Risk Level:</strong> {riskLevel}</p>
      <p><strong>Query Term:</strong> {getNestedValue(coinData, 'query_term')}</p>
      <p><strong>Full Text (if available):</strong> {getNestedValue(coinData, 'full_text', 'Not available')}</p>

      <ScoreBarChart data={scoreBreakdownData} title="Individual Score Breakdown" />
      
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
      
      {/* Placeholder for future enhancements or other charts */}
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

