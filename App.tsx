import React from 'react';
import './App.css';
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CoinListPage from './pages/CoinListPage';
import DashboardPage from './pages/DashboardPage';
import CoinDetailPage from './pages/CoinDetailPage';
import Layout from './components/Layout'; // Assuming a Layout component exists

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<CoinListPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/coins/:identifier" element={<CoinDetailPage />} />
          {/* Default route can be CoinListPage or DashboardPage */}
          <Route index element={<CoinListPage />} /> 
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

