import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import CoinDetailPage from './CoinDetailPage';
import * as apiService from '../services/apiService'; // Changed import to use * as
import { MemoryRouter, Routes, Route } from 'react-router-dom';

// Mock apiService
// The mock will automatically provide jest.fn() for all exports
jest.mock('../services/apiService');

// Mock Recharts components to avoid complex rendering in unit tests
jest.mock('recharts', () => ({
  ...jest.requireActual('recharts'),
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  Bar: () => <div data-testid="bar"></div>,
  XAxis: () => <div data-testid="x-axis"></div>,
  YAxis: () => <div data-testid="y-axis"></div>,
  CartesianGrid: () => <div data-testid="cartesian-grid"></div>,
  Tooltip: () => <div data-testid="tooltip"></div>,
  Legend: () => <div data-testid="legend"></div>,
}));

const mockCoinData = {
  user_screen_name: 'TestCoin',
  query_term: 'meme coin test',
  tweet_id: '12345tweet',
  full_text: 'This is a test tweet about a test coin.',
  overall_potential_score_0_10: 7.5,
  calculated_sentiment_score_0_10: 8.1,
  calculated_engagement_score_0_10: 6.5,
  context_financial_stability_score_0_10: 7.0,
  price_at_tweet_time: 0.001,
  volume_at_tweet_time: 100000,
  market_cap_at_tweet_time: 1000000,
  sma_20_day_feature: 0.0009,
  sma_50_day_feature: 0.0008,
  price_anomalies_count_feature: 1,
  volume_anomalies_count_feature: 0,
};

const renderWithRouter = (ui, { route = '/', path = '/' } = {}) => {
  window.history.pushState({}, 'Test page', route);
  return render(
    <MemoryRouter initialEntries={[route]}>
      <Routes>
        <Route path={path} element={ui} />
      </Routes>
    </MemoryRouter>
  );
};

describe('CoinDetailPage', () => {
  beforeEach(() => {
    // Reset mocks before each test
    // apiService.getCoinDetails.mockClear(); // Clear previous mock usage data
    jest.clearAllMocks(); // Clears all mocks, including implementation if set by mockReturnValue etc.
  });

  test('renders loading state initially', () => {
    apiService.getCoinDetails.mockReturnValue(new Promise(() => {})); // Keep promise pending
    renderWithRouter(<CoinDetailPage />, { route: '/coins/test-id', path: '/coins/:identifier' });
    expect(screen.getByText('Loading coin details for test-id...')).toBeInTheDocument();
  });

  test('renders error state if API call fails', async () => {
    apiService.getCoinDetails.mockRejectedValue(new Error('API Error'));
    renderWithRouter(<CoinDetailPage />, { route: '/coins/test-id', path: '/coins/:identifier' });
    await waitFor(() => {
      expect(screen.getByText('Error loading coin details: API Error')).toBeInTheDocument();
    });
  });

  test('renders "No data found" if API returns no data', async () => {
    apiService.getCoinDetails.mockResolvedValue({ data: null });
    renderWithRouter(<CoinDetailPage />, { route: '/coins/test-id', path: '/coins/:identifier' });
    await waitFor(() => {
      expect(screen.getByText('No data found for test-id.')).toBeInTheDocument();
    });
  });

  test('renders coin details and charts when data is fetched successfully', async () => {
    apiService.getCoinDetails.mockResolvedValue({ data: mockCoinData });
    renderWithRouter(<CoinDetailPage />, { route: '/coins/TestCoin', path: '/coins/:identifier' });

    await waitFor(() => {
      expect(screen.getByText('TestCoin - Details')).toBeInTheDocument();
    });

    // Check basic info
    expect(screen.getByText('Query Term: meme coin test')).toBeInTheDocument();
    expect(screen.getByText('Tweet ID: 12345tweet')).toBeInTheDocument();
    expect(screen.getByText('Full Text: This is a test tweet about a test coin.')).toBeInTheDocument();

    // Check score breakdown chart presence
    expect(screen.getByText('Individual Score Breakdown')).toBeInTheDocument();
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument(); // Mocked BarChart

    // Check scores overview
    expect(screen.getByText('Overall Potential Score (0-10): 7.5')).toBeInTheDocument();
    expect(screen.getByText('Calculated Sentiment Score (0-10): 8.1')).toBeInTheDocument();
    expect(screen.getByText('Calculated Engagement Score (0-10): 6.5')).toBeInTheDocument();
    expect(screen.getByText('Context Financial Stability Score (0-10): 7.0')).toBeInTheDocument();

    // Check financial context
    expect(screen.getByText('Price at Tweet Time: 0.001')).toBeInTheDocument();
    expect(screen.getByText('Volume at Tweet Time: 100000')).toBeInTheDocument();
    expect(screen.getByText('Market Cap at Tweet Time: 1000000')).toBeInTheDocument();
    expect(screen.getByText('SMA20 Feature: 0.0009')).toBeInTheDocument();
    expect(screen.getByText('SMA50 Feature: 0.0008')).toBeInTheDocument();
    expect(screen.getByText('Price Anomalies Count: 1')).toBeInTheDocument();
    expect(screen.getByText('Volume Anomalies Count: 0')).toBeInTheDocument();

    // Check placeholder sections
    expect(screen.getByText('Comparison to Average (Placeholder)')).toBeInTheDocument();
    expect(screen.getByText('Tokenomics (Placeholder from original file)')).toBeInTheDocument();
    expect(screen.getByText('Project Fundamentals (Placeholder from original file)')).toBeInTheDocument();
  });

  test('handles missing financial data gracefully', async () => {
    const partialData = { ...mockCoinData, price_at_tweet_time: undefined, volume_anomalies_count_feature: null };
    apiService.getCoinDetails.mockResolvedValue({ data: partialData });
    renderWithRouter(<CoinDetailPage />, { route: '/coins/PartialCoin', path: '/coins/:identifier' });

    await waitFor(() => {
      expect(screen.getByText('PartialCoin - Details')).toBeInTheDocument();
    });
    expect(screen.getByText('Price at Tweet Time: N/A')).toBeInTheDocument();
    expect(screen.getByText('Volume Anomalies Count: N/A')).toBeInTheDocument(); // Assuming null also renders as N/A
  });

});

