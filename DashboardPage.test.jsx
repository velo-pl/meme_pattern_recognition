import React from 'react';
import { render, screen } from '@testing-library/react';
import DashboardPage from './DashboardPage';
import useCoinStore from '../store/coinStore';
import { MemoryRouter } from 'react-router-dom'; // For Link components

// Mock the Zustand store
jest.mock('../store/coinStore');

// Mock Recharts components to avoid complex rendering in unit tests
// We are primarily testing data flow and conditional rendering, not Recharts internals
jest.mock('recharts', () => ({
  ...jest.requireActual('recharts'), // Import and retain default exports
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  Bar: () => <div data-testid="bar"></div>,
  XAxis: () => <div data-testid="x-axis"></div>,
  YAxis: () => <div data-testid="y-axis"></div>,
  CartesianGrid: () => <div data-testid="cartesian-grid"></div>,
  Tooltip: () => <div data-testid="tooltip"></div>,
  Legend: () => <div data-testid="legend"></div>,
  RadarChart: ({ children }) => <div data-testid="radar-chart">{children}</div>,
  PolarGrid: () => <div data-testid="polar-grid"></div>,
  PolarAngleAxis: () => <div data-testid="polar-angle-axis"></div>,
  PolarRadiusAxis: () => <div data-testid="polar-radius-axis"></div>,
  Radar: () => <div data-testid="radar"></div>,
}));

// Mock ErrorBoundary to just render children for testing purposes
jest.mock('../components/ErrorBoundary', () => ({ children }) => <>{children}</>);

describe('DashboardPage', () => {
  const mockFetchScores = jest.fn();

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    useCoinStore.mockReturnValue({
      scores: [],
      isLoading: false,
      error: null,
      fetchScores: mockFetchScores,
    });
  });

  test('renders loading state initially', () => {
    useCoinStore.mockReturnValueOnce({
      scores: [],
      isLoading: true,
      error: null,
      fetchScores: mockFetchScores,
    });
    render(<MemoryRouter><DashboardPage /></MemoryRouter>);
    expect(screen.getByText('Loading dashboard data...')).toBeInTheDocument();
  });

  test('fetches scores on mount if scores are empty', () => {
    render(<MemoryRouter><DashboardPage /></MemoryRouter>);
    expect(mockFetchScores).toHaveBeenCalledTimes(1);
  });

  test('does not fetch scores if scores are already present', () => {
    useCoinStore.mockReturnValueOnce({
        scores: [{ tweet_id: '1', overall_potential_score_0_10: 5 }], // Non-empty scores
        isLoading: false,
        error: null,
        fetchScores: mockFetchScores,
      });
    render(<MemoryRouter><DashboardPage /></MemoryRouter>);
    expect(mockFetchScores).not.toHaveBeenCalled();
  });

  test('renders error state', () => {
    useCoinStore.mockReturnValueOnce({
      scores: [],
      isLoading: false,
      error: 'Failed to fetch',
      fetchScores: mockFetchScores,
    });
    render(<MemoryRouter><DashboardPage /></MemoryRouter>);
    expect(screen.getByText('Error loading dashboard data: Failed to fetch')).toBeInTheDocument();
  });

  describe('Summary Statistics', () => {
    test('renders summary statistics with data', () => {
      const mockScores = [
        { overall_potential_score_0_10: 9 },
        { overall_potential_score_0_10: 7 },
        { overall_potential_score_0_10: 2 },
      ];
      useCoinStore.mockReturnValueOnce({
        scores: mockScores,
        isLoading: false,
        error: null,
        fetchScores: mockFetchScores,
      });
      render(<MemoryRouter><DashboardPage /></MemoryRouter>);
      expect(screen.getByText('Total Coins Analyzed: 3')).toBeInTheDocument();
      expect(screen.getByText('Promising Coins Identified: 1')).toBeInTheDocument(); // 9 >= 8
      expect(screen.getByText('High-Risk Coins Flagged: 1')).toBeInTheDocument(); // 2 <= 3
    });

    test('renders summary statistics with zero counts for empty scores', () => {
        useCoinStore.mockReturnValueOnce({
          scores: [],
          isLoading: false,
          error: null,
          fetchScores: mockFetchScores,
        });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('Total Coins Analyzed: 0')).toBeInTheDocument();
        expect(screen.getByText('Promising Coins Identified: 0')).toBeInTheDocument();
        expect(screen.getByText('High-Risk Coins Flagged: 0')).toBeInTheDocument();
      });
  });

  describe('Overall Potential Score Distribution Chart', () => {
    test('renders score distribution chart with data', () => {
        const mockScores = [{ overall_potential_score_0_10: 5 }];
        useCoinStore.mockReturnValueOnce({
          scores: mockScores,
          isLoading: false,
          error: null,
          fetchScores: mockFetchScores,
        });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('Overall Potential Score Distribution')).toBeInTheDocument();
        expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
      });

    test('renders "No data" message for score distribution chart when scores are empty', () => {
        useCoinStore.mockReturnValueOnce({
            scores: [],
            isLoading: false,
            error: null,
            fetchScores: mockFetchScores,
          });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('No data for score distribution.')).toBeInTheDocument();
      });
  });

  describe('Average Score Components (Radar) Chart', () => {
    test('renders radar chart with data', () => {
        const mockScores = [
            { calculated_sentiment_score_0_10: 7, calculated_engagement_score_0_10: 8, context_financial_stability_score_0_10: 6 }
        ];
        useCoinStore.mockReturnValueOnce({
          scores: mockScores,
          isLoading: false,
          error: null,
          fetchScores: mockFetchScores,
        });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('Average Score Components (Radar)')).toBeInTheDocument();
        expect(screen.getByTestId('radar-chart')).toBeInTheDocument();
      });
    
    test('renders "No data" message for radar chart when scores are empty', () => {
        useCoinStore.mockReturnValueOnce({
            scores: [],
            isLoading: false,
            error: null,
            fetchScores: mockFetchScores,
            });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('No data for average scores radar chart. Check console for data.')).toBeInTheDocument();
        });
  });

  describe('Top 5 Promising Coins Chart', () => {
    test('renders top promising coins chart with data', () => {
        const mockScores = [
            { user_screen_name: 'Coin1', overall_potential_score_0_10: 9, tweet_id: 't1' },
            { user_screen_name: 'Coin2', overall_potential_score_0_10: 8.5, tweet_id: 't2' },
        ];
        useCoinStore.mockReturnValueOnce({
          scores: mockScores,
          isLoading: false,
          error: null,
          fetchScores: mockFetchScores,
        });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('Top 5 Promising Coins')).toBeInTheDocument();
        // Since we mock BarChart, we check for its presence
        // The actual bars and data would be tested by checking the props passed to the mocked BarChart if needed
        expect(screen.getAllByTestId('bar-chart').length).toBeGreaterThanOrEqual(1); // One for distribution, one for top promising
      });

    test('renders "No promising coins" message when no coins meet criteria', () => {
        const mockScores = [
            { user_screen_name: 'CoinLow', overall_potential_score_0_10: 3, tweet_id: 't3' },
        ];
        useCoinStore.mockReturnValueOnce({
            scores: mockScores,
            isLoading: false,
            error: null,
            fetchScores: mockFetchScores,
            });
        render(<MemoryRouter><DashboardPage /></MemoryRouter>);
        expect(screen.getByText('No promising coins to display.')).toBeInTheDocument();
        });
  });

});

