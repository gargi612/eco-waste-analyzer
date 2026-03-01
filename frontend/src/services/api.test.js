import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { predictWaste, fetchAnalytics, calculateCarbon, apiClient } from './api';

// Create a new mock instance on the specific axios client created in api.js
const mock = new MockAdapter(apiClient);

describe('API Service Tests', () => {
    beforeEach(() => {
        // Reset the mock after each test
        mock.reset();
    });

    it('predictWaste() successfully processes mock file and returns valid response', async () => {
        const mockFile = new File(['dummy content'], 'test_waste.jpg', { type: 'image/jpeg' });
        const expectedResponse = {
            success: true,
            category: 'recyclable',
            confidence: 0.95,
            weight_grams: 100,
            co2_saved_grams: 120,
            eco_fact: 'Recycling saves energy!',
        };

        // The endpoint is /predict/
        mock.onPost('/predict/').reply(200, expectedResponse);

        const result = await predictWaste(mockFile, 100);
        expect(result).toEqual(expectedResponse);
        expect(result.success).toBe(true);
        expect(result.category).toBe('recyclable');
    });

    it('predictWaste() handles API errors gracefully', async () => {
        const mockFile = new File([''], 'test.jpg', { type: 'image/jpeg' });

        mock.onPost('/predict/').reply(500, {
            error: { message: 'Internal Server Error' }
        });

        await expect(predictWaste(mockFile, 100)).rejects.toThrow('Internal Server Error');
    });

    it('fetchAnalytics() returns valid dashboard data', async () => {
        const expectedResponse = {
            success: true,
            data: {
                total_scans: 42,
                total_co2_saved_kg: 5.4,
                breakdown: {
                    recyclable: 20,
                    biodegradable: 15,
                    hazardous: 7
                }
            }
        };

        mock.onGet('/analytics/dashboard').reply(200, expectedResponse);

        const result = await fetchAnalytics();
        expect(result).toEqual(expectedResponse);
        expect(result.data.total_scans).toBe(42);
    });

    it('calculateCarbon() returns calculated CO2 savings', async () => {
        const expectedResponse = {
            success: true,
            category: 'biodegradable',
            weight_grams: 500,
            co2_saved_grams: 250,
            co2_saved_kg: 0.25,
            eco_fact: 'Compost!'
        };

        mock.onPost('/carbon/calculate').reply(200, expectedResponse);

        const result = await calculateCarbon('biodegradable', 500);
        expect(result).toEqual(expectedResponse);
        expect(result.co2_saved_grams).toBe(250);
    });
});
