// test_api.js
// Run this file using Node.js to verify frontend API mocking logic without Vite
// node test_api.js

import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/v1';

async function testFrontendBindings() {
    console.log("====================================");
    console.log("TESTING FRONTEND API BINDINGS");
    console.log("Ensure backend is running on port 8000");
    console.log("====================================\n");

    try {
        // 1. Test Carbon Fetch
        console.log("--- Testing calculateCarbon() Mock ---");
        const carbonRes = await axios.post(`${BASE_URL}/carbon/calculate`, {
            category: "hazardous",
            weight_grams: 50
        });
        console.log("✅ Carbon API Mock Success:", carbonRes.data);

        // 2. Test Analytics Fetch
        console.log("\n--- Testing fetchAnalytics() Mock ---");
        const analyticsRes = await axios.get(`${BASE_URL}/analytics/dashboard`);
        console.log("✅ Analytics API Mock Success! Total Scans:", analyticsRes.data.data.total_scans);

    } catch (error) {
        console.error("❌ MOCK API TEST FAILED:", error.message);
        if (error.code === 'ECONNREFUSED') {
            console.error("The backend server is not running on port 8000.");
        }
    }
}

testFrontendBindings();
