import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'; // Our Flask backend

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getScores = () => {
  return apiClient.get('/scores');
};

export const getCoinDetailsByIdentifier = (identifier) => {
  return apiClient.get(`/scores/${identifier}`);
};

// Add other API service functions as needed

