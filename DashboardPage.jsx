import React, { useEffect, useMemo } from 'react';
import useCoinStore from '../store/coinStore';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'; // Added Radar to imports
import ErrorBoundary from '../components/ErrorBoundary'; // Import ErrorBoundary

const DashboardPage = () => {
  const { scores, isLoading, error, fetchScores } = useCoinStore();

  useEffect(() => {
    if (scores.length === 0) {
      fetchScores();
    }
  }, [fetchScores, scores.length]);

  const summaryStats = useMemo(() => {
    if (!scores || scores.length === 0) {
      return {
        totalAnalyzed: 0,
        promisingCount: 0,
        highRiskCount: 0,
      };
    }
    const promisingThreshold = 8;
    const highRiskThreshold = 3;
    const promisingCoins = scores.filter(coin => coin.overall_potential_score_0_10 >= promisingThreshold);
    const highRiskCoins = scores.filter(coin => coin.overall_potential_score_0_10 <= highRiskThreshold);
    return {
      totalAnalyzed: scores.length,
      promisingCount: promisingCoins.length,
      highRiskCount: highRiskCoins.length,
    };
  }, [scores]);

  const topPromisingCoins = useMemo(() => {
    if (!scores || scores.length === 0) return [];
    const filteredSorted = [...scores]
      .filter(coin => coin.overall_potential_score_0_10 >= 8 && coin.user_screen_name)
      .sort((a, b) => b.overall_potential_score_0_10 - a.overall_potential_score_0_10)
      .slice(0, 5);
    return filteredSorted.map(coin => ({ 
        user_screen_name: coin.user_screen_name || 'Unknown',
        overall_potential_score_0_10: coin.overall_potential_score_0_10 || 0,
        tweet_id: coin.tweet_id 
      }));
  }, [scores]);

  const scoreDistributionData = useMemo(() => { 
    if (!scores || scores.length === 0) return [];
    const bins = [
      { name: '0-2', count: 0 },
      { name: '2-4', count: 0 },
      { name: '4-6', count: 0 },
      { name: '6-8', count: 0 },
      { name: '8-10', count: 0 },
    ];
    scores.forEach(coin => {
      const score = coin.overall_potential_score_0_10;
      if (score >= 0 && score <= 2) bins[0].count++;
      else if (score > 2 && score <= 4) bins[1].count++;
      else if (score > 4 && score <= 6) bins[2].count++;
      else if (score > 6 && score <= 8) bins[3].count++;
      else if (score > 8 && score <= 10) bins[4].count++;
    });
    return bins;
  }, [scores]);

  const averageScoresData = useMemo(() => { 
    if (!scores || scores.length === 0) return [
        { name: 'Sentiment', score: 0 },
        { name: 'Engagement', score: 0 },
        { name: 'Stability', score: 0 },
    ];
    const numScores = scores.length;
    if (numScores === 0) return [
        { name: 'Sentiment', score: 0 },
        { name: 'Engagement', score: 0 },
        { name: 'Stability', score: 0 },
    ];
    const avgSentiment = scores.reduce((acc, coin) => acc + (coin.calculated_sentiment_score_0_10 || 0), 0) / numScores;
    const avgEngagement = scores.reduce((acc, coin) => acc + (coin.calculated_engagement_score_0_10 || 0), 0) / numScores;
    const avgStability = scores.reduce((acc, coin) => acc + (coin.context_financial_stability_score_0_10 || 0), 0) / numScores;
    const result = [
      { name: 'Sentiment', score: parseFloat(avgSentiment.toFixed(2)) },
      { name: 'Engagement', score: parseFloat(avgEngagement.toFixed(2)) },
      { name: 'Stability', score: parseFloat(avgStability.toFixed(2)) },
    ];
    console.log('Average Scores Data:', result);
    return result;
  }, [scores]);

  const radarChartData = useMemo(() => { 
    if (!averageScoresData || averageScoresData.some(d => d.score === undefined || isNaN(d.score))) {
        console.log('RadarChartData: averageScoresData is invalid or empty', averageScoresData);
        return []; 
    }
    const mappedData = averageScoresData.map(item => ({ subject: item.name, A: item.score, fullMark: 10 }));
    console.log('RadarChartData (mapped):', mappedData);
    return mappedData;
  }, [averageScoresData]);

  const highRiskAlerts = useMemo(() => {
    if (!scores || scores.length === 0) return [];
    return [...scores]
      .filter(coin => coin.overall_potential_score_0_10 <= 3)
      .sort((a, b) => a.overall_potential_score_0_10 - b.overall_potential_score_0_10)
      .slice(0, 5);
  }, [scores]);

  if (isLoading && scores.length === 0) {
    return <p>Loading dashboard data...</p>;
  }

  if (error) {
    return <p>Error loading dashboard data: {typeof error === 'object' ? JSON.stringify(error) : error}</p>;
  }
  
  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome to the Meme Coin Pattern Recognition Platform dashboard.</p>

      {/* Row 1: Summary Statistics and Score Distribution */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
        <ErrorBoundary sectionName="Summary Statistics">
          <div style={{ flex: 1, minWidth: '300px', padding: '10px', border: '1px solid #ccc' }}>
            <h3>Summary Statistics</h3>
            <p>Total Coins Analyzed: {summaryStats.totalAnalyzed}</p>
            <p>Promising Coins Identified: {summaryStats.promisingCount}</p>
            <p>High-Risk Coins Flagged: {summaryStats.highRiskCount}</p>
          </div>
        </ErrorBoundary>

        <ErrorBoundary sectionName="Overall Potential Score Distribution Chart">
          <div style={{ flex: 1, minWidth: '300px', padding: '10px', border: '1px solid #ccc' }}>
            <h3>Overall Potential Score Distribution</h3>
            {scores.length > 0 && scoreDistributionData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={scoreDistributionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#8884d8" name="Number of Coins" />
                </BarChart>
              </ResponsiveContainer>
            ) : <p>No data for score distribution.</p>}
          </div>
        </ErrorBoundary>
      </div>

      {/* Row 2: Radar Chart and Top Promising Coins */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
        <ErrorBoundary sectionName="Average Score Components (Radar) Chart">
          <div style={{ flex: 1, minWidth: '300px', padding: '10px', border: '1px solid #ccc' }}>
            <h3>Average Score Components (Radar)</h3>
            {scores.length > 0 && radarChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarChartData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={30} domain={[0, 10]}/>
                  <Radar name="Average Scores" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                  <Tooltip />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            ) : <p>No data for average scores radar chart. Check console for data.</p>}
          </div>
        </ErrorBoundary>

        <ErrorBoundary sectionName="Top Promising Coins Chart">
          <div style={{ flex: 1, minWidth: '300px', padding: '10px', border: '1px solid #ccc' }}>
            <h3>Top 5 Promising Coins</h3>
            {topPromisingCoins.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={topPromisingCoins} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" domain={[0, 10]} />
                  <YAxis dataKey="user_screen_name" type="category" interval={0} width={100} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="overall_potential_score_0_10" fill="#82ca9d" name="Overall Score" />
                </BarChart>
              </ResponsiveContainer>
            ) : <p>No promising coins to display.</p>}
          </div>
        </ErrorBoundary>
      </div>

      {/* Row 3: High-Risk Alerts - Still commented out */}
      {/* <ErrorBoundary sectionName="High-Risk Alerts"> */}
      {/*   <div style={{ marginTop: '20px
olpadding: '10px', border: '1px solid #ccc' }}> */}
      {/*     <h3>High-Risk Alerts</h3> */}
      {/*     {highRiskAlerts.length > 0 ? ( */}
      {/*       <ul> */}
      {/*         {highRiskAlerts.map((coin, index) => ( */}
      {/*           <li key={coin.user_screen_name || `risk-${index}`}>
                    <Link to={`/coins/${coin.user_screen_name || coin.tweet_id}`}>
                      {coin.user_screen_name || 'Unknown Coin'} (Score: {coin.overall_potential_score_0_10.toFixed(2)})
                    </Link>
                  </li> */}
      {/*         ))} */}
      {/*       </ul> */}
      {/*     ) : ( */}
      {/*       <p>No high-risk coins found based on current criteria.</p> */}
      {/*     )} */}
      {/*   </div> */}
      {/* </ErrorBoundary> */}

    </div>
  );
};

export default DashboardPage;

