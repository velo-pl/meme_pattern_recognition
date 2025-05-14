import React, { useEffect, useState } from 'react';
import useCoinStore from '../store/coinStore';
import axios from 'axios'; // Import axios for direct API call test

const CoinListPage = () => {
  const { scores, isLoading, error, fetchScores } = useCoinStore();
  const [directApiResponse, setDirectApiResponse] = useState(null);
  const [directApiError, setDirectApiError] = useState(null);

  useEffect(() => {
    // Original fetch via Zustand store
    fetchScores();

    // Direct API call for debugging
    const testDirectApiCall = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/v1/scores');
        setDirectApiResponse(response.data);
      } catch (e) {
        setDirectApiError(e.message || 'Direct API call failed');
      }
    };
    testDirectApiCall();

  }, [fetchScores]);

  // UI for debugging state
  const renderDebugInfo = () => (
    <div style={{ border: '2px solid red', margin: '10px', padding: '10px', fontFamily: 'monospace', fontSize: '12px' }}>
      <h4>Debug Information (Zustand Store):</h4>
      <p>isLoading: {isLoading.toString()}</p>
      <p>error: {error ? JSON.stringify(error) : 'null'}</p>
      <p>scores is Array: {Array.isArray(scores).toString()}</p>
      <p>scores length: {(scores && Array.isArray(scores)) ? scores.length : 'N/A (or not an array)'}</p>
      <p>scores content:</p>
      <pre style={{ maxHeight: '100px', overflowY: 'auto', backgroundColor: '#f0f0f0', padding: '5px', border: '1px solid #ccc' }}>
        {JSON.stringify(scores, null, 2)}
      </pre>
      <h4>Debug Information (Direct API Call):</h4>
      <p>Direct API Error: {directApiError ? directApiError : 'null'}</p>
      <p>Direct API Response:</p>
      <pre style={{ maxHeight: '100px', overflowY: 'auto', backgroundColor: '#e0e0e0', padding: '5px', border: '1px solid #aaa' }}>
        {JSON.stringify(directApiResponse, null, 2)}
      </pre>
    </div>
  );

  if (isLoading && !directApiResponse && !directApiError) return <><p>Loading coins...</p>{renderDebugInfo()}</>;
  if (error && !directApiResponse && !directApiError) return <><p>Error fetching coins (Zustand): {typeof error === 'object' ? JSON.stringify(error) : error}</p>{renderDebugInfo()}</>;
  
  if (!scores || !Array.isArray(scores) || scores.length === 0) {
    return <><p>No coins found (from Zustand store).</p>{renderDebugInfo()}</>;
  }

  return (
    <div>
      {renderDebugInfo()} 
      <h2>Coin List & Exploration</h2>
      <p>Browse, sort, and filter all analyzed meme coins. (Data from API)</p>
      <div style={{ marginTop: '20px' }}>
        <input type="text" placeholder="Filter by name, symbol..." style={{ marginBottom: '10px', padding: '8px', width: '300px' }} />
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>User/Screen Name</th>
            <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>Overall Potential Score</th>
            <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>Sentiment Score (0-10)</th>
            <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>Engagement Score (0-10)</th>
            <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>Financial Stability (0-10)</th>
          </tr>
        </thead>
        <tbody>
          {scores.map((coin, index) => (
            <tr key={coin.tweet_id || coin.user_screen_name || `coin-${index}`}>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{coin.user_screen_name || 'N/A'}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{coin.overall_potential_score_0_10 !== undefined ? coin.overall_potential_score_0_10.toFixed(2) : 'N/A'}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{coin.calculated_sentiment_score_0_10 !== undefined ? coin.calculated_sentiment_score_0_10.toFixed(2) : 'N/A'}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{coin.calculated_engagement_score_0_10 !== undefined ? coin.calculated_engagement_score_0_10.toFixed(2) : 'N/A'}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{coin.context_financial_stability_score_0_10 !== undefined ? coin.context_financial_stability_score_0_10.toFixed(2) : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CoinListPage;

