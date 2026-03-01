import axios from 'axios';

const PROD_API = import.meta.env.VITE_API_URL || 'https://waste-analyzer-backend.onrender.com/api/v1'; // Replace with actual backend deployment
const DEV_API = 'http://localhost:8000/api/v1';
const API_BASE_URL = import.meta.env.PROD ? PROD_API : DEV_API;

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictWaste = async (imageFile, weightGrams = 100) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('weight_grams', weightGrams.toString());

    try {
        const response = await apiClient.post('/predict/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error?.message || 'Failed to analyze waste. Ensure the backend is running.');
    }
};

export const fetchAnalytics = async () => {
    try {
        const response = await apiClient.get('/analytics/dashboard');
        return response.data;
    } catch (error) {
        throw new Error('Failed to fetch analytics data.');
    }
};

export const calculateCarbon = async (category, weightGrams) => {
    try {
        const response = await apiClient.post('/carbon/calculate', {
            category,
            weight_grams: weightGrams,
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to calculate carbon savings.');
    }
};
