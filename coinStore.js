import { create } from 'zustand';
import { getScores } from '../services/apiService';

const useCoinStore = create((set, get) => ({ 
  scores: [],
  isLoading: false,
  error: null,
  fetchScores: async () => {
    if (get().isLoading) {
      return;
    }
    set({ isLoading: true, error: null });
    try {
      const response = await getScores(); // AxiosResponse object
      
      let apiData = response.data; // This should be the parsed JSON object if server Content-Type is correct

      // If apiData is a string, it means it wasn't auto-parsed by Axios or was double-stringified.
      if (typeof apiData === 'string') {
        try {
          apiData = JSON.parse(apiData); // Attempt to parse it
        } catch (parseError) {
          console.error('Failed to parse API response string:', parseError); // For server-side logging if possible
          set({ error: `Failed to parse API response: ${parseError.message}`, isLoading: false, scores: [] });
          return;
        }
      }

      let fetchedScores = []; 
      if (apiData && Array.isArray(apiData.scores)) {
        fetchedScores = apiData.scores;
      } else {
        console.error('apiData.scores is not an array or apiData/apiData.scores is missing. apiData:', apiData);
        // Set an error or keep scores empty if the expected structure isn't found
        // This helps differentiate from a successful fetch of an empty list from the API itself.
        set({ error: 'Unexpected API response structure', isLoading: false, scores: [] });
        return;
      }
      
      set({ scores: fetchedScores, isLoading: false });

    } catch (error) {
      console.error('Error fetching scores in store:', error);
      let errorMessage = 'Failed to fetch scores';
      if (error.response) {
        errorMessage = `Server error: ${error.response.status} - ${JSON.stringify(error.response.data)}`;
      } else if (error.request) {
        errorMessage = 'No response from server. Check network or CORS.';
      } else if (error.message) {
        errorMessage = error.message;
      }
      set({ error: errorMessage, isLoading: false, scores: [] });
    }
  },
}));

export default useCoinStore;

