import React, { useState } from 'react';
import { Send, Globe, Database, Clock, ShieldCheck } from 'lucide-react';
import { Button } from '../../components/ui';

export const ApiTester = () => {
    const [method, setMethod] = useState('GET');
    const [url, setUrl] = useState('');
    const [body, setBody] = useState('{\n  "key": "value"\n}');
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSend = async () => {
        setLoading(true);
        setError(null);
        setResponse(null);
        try {
            let parsedBody = null;
            if (['POST', 'PUT'].includes(method)) {
                try {
                    parsedBody = JSON.parse(body);
                } catch (e) {
                    throw new Error("Invalid JSON body");
                }
            }

            const res = await fetch('/api/v1/test-api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    method,
                    url,
                    body: parsedBody
                })
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Request failed");
            setResponse(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid grid-cols-12 gap-8 animate-in fade-in duration-500">
            {/* Control Panel */}
            <div className="col-span-12 lg:col-span-5 flex flex-col gap-6">
                <div className="bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-sm border border-gray-200 dark:border-gray-700">
                    <h3 className="text-sm font-bold flex items-center gap-2 mb-6">
                        <Globe className="w-4 h-4 text-primary-500" /> Request Configuration
                    </h3>

                    <div className="flex flex-col gap-4">
                        <div className="flex gap-2">
                            <select
                                value={method}
                                onChange={(e) => setMethod(e.target.value)}
                                className="bg-gray-50 dark:bg-gray-900 px-4 py-3 rounded-2xl text-xs font-bold border border-gray-200 dark:border-gray-700 outline-none focus:ring-2 focus:ring-primary-500 transition-all w-32"
                            >
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                                <option value="PUT">PUT</option>
                                <option value="DELETE">DELETE</option>
                            </select>
                            <input
                                type="text"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="https://api.example.com/data"
                                className="flex-1 bg-gray-50 dark:bg-gray-900 px-6 py-3 rounded-2xl text-xs font-mono border border-gray-200 dark:border-gray-700 outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                            />
                        </div>

                        {['POST', 'PUT'].includes(method) && (
                            <div className="flex flex-col gap-2">
                                <label className="text-[10px] font-bold text-gray-400 uppercase ml-2">JSON Body</label>
                                <textarea
                                    value={body}
                                    onChange={(e) => setBody(e.target.value)}
                                    className="h-64 bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl text-xs font-mono border border-gray-200 dark:border-gray-700 outline-none focus:ring-2 focus:ring-primary-500 transition-all resize-none"
                                />
                            </div>
                        )}

                        <Button
                            onClick={handleSend}
                            disabled={loading || !url}
                            icon={Send}
                            className="w-full mt-4 py-4"
                        >
                            {loading ? 'Sending...' : 'Send Request'}
                        </Button>
                    </div>
                </div>

                {error && (
                    <div className="p-4 bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-900/40 rounded-2xl text-rose-600 dark:text-rose-400 text-xs font-bold animate-in slide-in-from-top duration-300">
                        Error: {error}
                    </div>
                )}
            </div>

            {/* Output Panel */}
            <div className="col-span-12 lg:col-span-7">
                {response ? (
                    <div className="flex flex-col gap-6 h-full">
                        <div className="grid grid-cols-3 gap-4">
                            <StatCard label="Status" value={response.status_code} color={response.status_code < 300 ? 'text-emerald-500' : 'text-rose-500'} />
                            <StatCard label="Time" value={`${response.time_ms}ms`} color="text-amber-500" />
                            <StatCard label="Size" value="N/A" color="text-indigo-500" />
                        </div>

                        <div className="flex-1 bg-white dark:bg-gray-800 rounded-3xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col">
                            <div className="px-8 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-900/50">
                                <h4 className="text-[10px] font-bold uppercase tracking-wider text-gray-400">Response Body</h4>
                                <span className="text-[10px] font-mono text-gray-400">JSON</span>
                            </div>
                            <div className="flex-1 p-8 overflow-auto font-mono text-xs text-gray-600 dark:text-gray-400 bg-gray-50/20">
                                <pre>{JSON.stringify(response.data, null, 2)}</pre>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="h-full bg-white dark:bg-gray-800 rounded-[3rem] border-2 border-dashed border-gray-100 dark:border-gray-700 flex flex-col items-center justify-center text-center p-12">
                        <div className="p-6 bg-gray-50 dark:bg-gray-900 rounded-full mb-6">
                            <Database className="w-12 h-12 text-gray-200" />
                        </div>
                        <h4 className="text-xl font-black text-gray-300">No Response Data</h4>
                        <p className="text-gray-400 text-xs mt-2 max-w-[200px]">Send a request on the left to inspect HTTP responses and headers.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

const StatCard = ({ label, value, color }) => (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-widest block mb-1">{label}</span>
        <span className={`text-xl font-black ${color}`}>{value}</span>
    </div>
);
