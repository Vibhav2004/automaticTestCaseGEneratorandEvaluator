import { useState, useEffect } from 'react';
import api from '../services/api';

export const useAutoTest = () => {
    const [code, setCode] = useState('def add(a: int, b: int):\n    return a + b');
    const [language, setLanguage] = useState('python');
    const [functions, setFunctions] = useState([]);
    const [testCases, setTestCases] = useState([]);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [sessions, setSessions] = useState([]);

    // Initialize history
    useEffect(() => {
        const saved = localStorage.getItem('autotest_sessions');
        if (saved) setSessions(JSON.parse(saved));
    }, []);

    const handleAnalyze = async () => {
        setLoading(true);
        setError(null);
        setResults(null);
        try {
            const data = await api.analyze(code, language);
            setFunctions(data.functions);

            const tests = await api.generateTests({
                functions: data.functions,
                conditions: data.conditions,
                literals: data.literals
            });
            setTestCases(tests);

            if (tests.length === 0) {
                setError("No tests could be generated for the detected functions.");
            }
            return true;
        } catch (err) {
            const detail = err.response?.data?.detail || err.message || "Analysis failed";
            setError(detail);
            return false;
        } finally {
            setLoading(false);
        }
    };

    const handleExecute = async () => {
        setLoading(true);
        setError(null);
        try {
            const sessionResult = await api.execute(code, language, testCases);
            setResults(sessionResult);

            const newSession = {
                id: sessionResult.session_id,
                timestamp: new Date().toISOString(),
                language,
                ...sessionResult
            };
            const updated = [newSession, ...sessions.slice(0, 19)]; // Keep last 20
            setSessions(updated);
            localStorage.setItem('autotest_sessions', JSON.stringify(updated));
            return true;
        } catch (err) {
            const detail = err.response?.data?.detail || err.message || "Execution failed";
            setError(detail);
            return false;
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const content = event.target.result;
            setCode(content);
            const ext = file.name.split('.').pop().toLowerCase();
            const langMap = { 'py': 'python', 'java': 'java', 'js': 'javascript', 'cpp': 'cpp', 'cs': 'csharp', 'go': 'go' };
            if (langMap[ext]) setLanguage(langMap[ext]);
        };
        reader.readAsText(file);
    };

    const [webUrl, setWebUrl] = useState('');
    const [webResults, setWebResults] = useState(null);

    const handleWebTest = async () => {
        if (!webUrl) {
            setError("Please enter a website URL");
            return;
        }
        setLoading(true);
        setError(null);
        setWebResults(null);
        try {
            const data = await api.testWebsite(webUrl);
            setWebResults(data);
            return true;
        } catch (err) {
            const detail = err.response?.data?.detail || err.message || "Web testing failed";
            setError(detail);
            return false;
        } finally {
            setLoading(false);
        }
    };

    return {
        code, setCode,
        language, setLanguage,
        functions, testCases,
        results, setResults,
        loading, error, setError,
        sessions, setSessions,
        webUrl, setWebUrl,
        webResults, setWebResults,
        handleAnalyze, handleExecute, handleFileUpload, handleWebTest
    };
};
