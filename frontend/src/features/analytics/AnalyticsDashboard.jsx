import React from 'react';
import {
    PieChart, Pie, Cell, ResponsiveContainer,
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';
import { Terminal, Zap, Download } from 'lucide-react';
import { StatCard } from '../../components/ui';

const COLORS = ['#10b981', '#ef4444', '#f59e0b'];

export const AnalyticsDashboard = ({ results }) => {
    if (!results) return null;

    const pieData = [
        { name: 'Pass', value: results.passed_tests },
        { name: 'Fail', value: results.failed_tests },
        { name: 'Error', value: results.error_tests },
    ];

    const barData = results.results.map((r, i) => ({
        name: `T${i + 1}`,
        time: r.execution_time
    }));

    const downloadJsonReport = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(results, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", `report_${results.session_id}.json`);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    return (
        <div className="flex flex-col gap-8 animate-in fade-in duration-500">
            <div className="grid grid-cols-3 gap-6">
                <StatCard label="Total Tests" value={results.total_tests} color="text-indigo-500" icon={Zap} />
                <StatCard label="Success Rate" value={`${Math.round((results.passed_tests / (results.total_tests || 1)) * 100)}%`} color="text-emerald-500" />
                <StatCard label="Avg. Latency" value={`${results.avg_execution_time}s`} color="text-amber-500" />
            </div>

            <div className="grid grid-cols-2 gap-6 h-80">
                <ChartContainer title="Outcome Distribution">
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie data={pieData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                                {pieData.map((_, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip contentStyle={{ borderRadius: '16px', border: 'none', background: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(4px)' }} />
                        </PieChart>
                    </ResponsiveContainer>
                </ChartContainer>

                <ChartContainer title="Performance (Seconds)">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={barData}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" className="dark:stroke-gray-800" />
                            <XAxis dataKey="name" fontSize={10} axisLine={false} tickLine={false} />
                            <YAxis fontSize={10} axisLine={false} tickLine={false} />
                            <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: '12px', border: 'none' }} />
                            <Bar dataKey="time" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartContainer>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-sm font-bold flex items-center gap-2">
                        <Terminal className="w-4 h-4 text-primary-500" /> Detailed Test Log
                    </h3>
                    <button
                        onClick={downloadJsonReport}
                        className="text-[10px] font-bold text-primary-500 hover:text-primary-600 px-3 py-1 bg-primary-50 dark:bg-primary-900/20 rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Download className="w-3 h-3" /> Export JSON
                    </button>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead>
                            <tr className="border-b border-gray-100 dark:border-gray-700">
                                <th className="pb-4 font-semibold text-gray-400 uppercase text-[10px]">Test ID</th>
                                <th className="pb-4 font-semibold text-gray-400 uppercase text-[10px]">Inputs</th>
                                <th className="pb-4 font-semibold text-gray-400 uppercase text-[10px]">Result</th>
                                <th className="pb-4 font-semibold text-gray-400 uppercase text-[10px]">Status</th>
                                <th className="pb-4 font-semibold text-gray-400 uppercase text-[10px]">Diagnosis</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-50 dark:divide-gray-800">
                            {results.results.map((r, i) => (
                                <tr key={i} className="group hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors">
                                    <td className="py-4 font-mono text-[10px] text-gray-400">{r.test_id}</td>
                                    <td className="py-4 font-mono text-[10px] truncate max-w-[120px]">{JSON.stringify(r.input_values)}</td>
                                    <td className="py-4 font-mono text-[10px] text-gray-500 overflow-hidden text-ellipsis whitespace-nowrap max-w-[150px]">
                                        {r.actual_output !== null ? String(r.actual_output) : '-'}
                                    </td>
                                    <td className="py-4">
                                        <Badge status={r.status} />
                                    </td>
                                    <td className="py-4 text-[10px] text-gray-500 max-w-[200px] leading-relaxed italic">
                                        {r.diagnosis || (r.status === 'PASS' ? 'Logic verified.' : '')}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

const ChartContainer = ({ title, children }) => (
    <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col">
        <h4 className="text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-6">{title}</h4>
        {children}
    </div>
);

const Badge = ({ status }) => {
    const styles = {
        PASS: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400',
        FAIL: 'bg-rose-100 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400',
        ERROR: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400'
    };
    return (
        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${styles[status]}`}>
            {status}
        </span>
    );
};
