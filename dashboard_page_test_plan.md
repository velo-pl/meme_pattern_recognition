## Component and Unit Test Plan for DashboardPage Charts

This document outlines the test plan for the chart components implemented on the `DashboardPage` of the Meme Coin Pattern Recognition Platform.

**Testing Framework:** Jest and React Testing Library (assuming standard Create React App / Vite setup).

**Target Component:** `DashboardPage.jsx` (specifically the chart rendering sections)

**Overall Goals:**
*   Ensure chart components render correctly with various data inputs (valid, empty, edge cases).
*   Verify that data processing logic (e.g., in `useMemo` hooks) transforms data as expected.
*   Confirm that loading and error states are handled gracefully.
*   Ensure chart elements (axes, legends, tooltips, bars, radar areas) are present and display correct information where applicable.
*   Test the functionality of `ErrorBoundary` components wrapping each chart.

**Specific Test Cases:**

**1. Summary Statistics Section:**
    *   Test 1.1: Renders correctly with valid `summaryStats` data.
    *   Test 1.2: Displays correct numbers for "Total Coins Analyzed", "Promising Coins Identified", and "High-Risk Coins Flagged".
    *   Test 1.3: Renders correctly when `scores` are empty (initial state or no data).

**2. Overall Potential Score Distribution Chart (BarChart):**
    *   Test 2.1: Renders the chart when `scoreDistributionData` is valid and non-empty.
    *   Test 2.2: Displays the "No data for score distribution." message when `scoreDistributionData` is empty.
    *   Test 2.3: Verifies that XAxis, YAxis, Tooltip, Legend, and Bar components are rendered.
    *   Test 2.4: Mocks `scores` data and verifies that `scoreDistributionData` hook calculates bin counts correctly.
    *   Test 2.5: Checks if the `ErrorBoundary` catches and displays an error if the chart throws one (requires a way to mock a chart error).

**3. Average Score Components (RadarChart):**
    *   Test 3.1: Renders the chart when `radarChartData` is valid and non-empty.
    *   Test 3.2: Displays the "No data for average scores radar chart." message when `radarChartData` is empty.
    *   Test 3.3: Verifies that PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip, and Legend components are rendered.
    *   Test 3.4: Mocks `scores` data and verifies that `averageScoresData` and `radarChartData` hooks calculate and map data correctly (e.g., correct subjects, scores, fullMark).
    *   Test 3.5: Checks if the `ErrorBoundary` catches and displays an error if the chart throws one.

**4. Top 5 Promising Coins Chart (BarChart - Vertical):**
    *   Test 4.1: Renders the chart when `topPromisingCoins` data is valid and non-empty.
    *   Test 4.2: Displays the "No promising coins to display." message when `topPromisingCoins` is empty.
    *   Test 4.3: Verifies that XAxis, YAxis, Tooltip, Legend, and Bar components are rendered.
    *   Test 4.4: Mocks `scores` data and verifies that `topPromisingCoins` hook filters, sorts, and maps data correctly (e.g., correct coin names, scores, top 5 limit).
    *   Test 4.5: Checks if the `ErrorBoundary` catches and displays an error if the chart throws one.

**5. General `DashboardPage` Tests:**
    *   Test 5.1: Displays "Loading dashboard data..." when `isLoading` is true and `scores` are empty.
    *   Test 5.2: Displays an error message when the `error` prop is set.
    *   Test 5.3: Verifies that `fetchScores` is called on initial render if scores are empty (mock `useCoinStore`).

**Mocking Strategy:**
*   `useCoinStore`: Mock this Zustand store to provide controlled `scores`, `isLoading`, and `error` states, and to spy on `fetchScores`.
*   Recharts components: Generally, we will test that they are rendered. For more complex interactions, we might need to mock specific Recharts functionalities if direct testing becomes too difficult, but the primary focus will be on data flow and conditional rendering.

**Next Steps:**
1.  Create `DashboardPage.test.jsx`.
2.  Set up necessary mocks (especially for `useCoinStore`).
3.  Implement the test cases outlined above, starting with the data processing hooks and then moving to the rendering of chart sections.

