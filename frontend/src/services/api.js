import axios from 'axios';

const API_BASE = '/api/v1';

const api = {
    analyze: async (code, language) => {
        const response = await axios.post(`${API_BASE}/analyze`, { code, language });
        return response.data;
    },
    generateTests: async (requestBody) => {
        const response = await axios.post(`${API_BASE}/generate-tests`, requestBody);
        return response.data;
    },
    execute: async (code, language, testCases) => {
        const response = await axios.post(`${API_BASE}/execute`, { code, language, test_cases: testCases });
        return response.data;
    },
    testWebsite: async (url) => {
        const response = await axios.post(`${API_BASE}/test-website`, { url });
        return response.data;
    }
};

export default api;
