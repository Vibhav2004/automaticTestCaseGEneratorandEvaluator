import React from 'react';
import { History, Trash2 } from 'lucide-react';

export const HistorySection = ({ sessions, setSessions, onSelectSession }) => {
    return (
        <div className="col-span-12 animate-in slide-in-from-bottom-4 duration-500">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-xl font-bold flex items-center gap-3">
                    <History className="w-6 h-6 text-primary-500" />
                    Execution History
                </h2>
                {sessions.length > 0 && (
                    <button
                        onClick={() => {
                            setSessions([]);
                            localStorage.removeItem('autotest_sessions');
                        }}
                        className="text-xs font-bold text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/10 px-4 py-2 rounded-xl transition-colors flex items-center gap-2"
                    >
                        <Trash2 className="w-4 h-4" /> Clear History
                    </button>
                )}
            </div>

            {sessions.length === 0 ? (
                <div className="bg-white dark:bg-gray-800 rounded-3xl p-16 text-center border-2 border-dashed border-gray-200 dark:border-gray-700">
                    <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-full w-fit mx-auto mb-4">
                        <History className="w-8 h-8 text-gray-300" />
                    </div>
                    <h3 className="text-lg font-bold">No history available</h3>
                    <p className="text-gray-500 text-sm max-w-xs mx-auto">Run some tests in the editor to see your session reports here for comparison.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {sessions.map((s) => (
                        <div
                            key={s.id}
                            className="bg-white dark:bg-gray-800 rounded-3xl p-6 border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:shadow-primary-500/5 transition-all group cursor-pointer active:scale-95"
                            onClick={() => onSelectSession(s)}
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div className="flex flex-col">
                                    <span className="text-[10px] font-bold text-primary-500 uppercase tracking-widest">{s.language}</span>
                                    <span className="text-xs text-gray-400 font-medium">{new Date(s.timestamp).toLocaleDateString()} at {new Date(s.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                                </div>
                                <div className={`px-2 py-1 rounded-lg text-[10px] font-bold ${(s.passed_tests / (s.total_tests || 1)) >= 0.8 ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-600'}`}>
                                    {Math.round((s.passed_tests / (s.total_tests || 1)) * 100)}% Pass
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div className="h-1.5 bg-gray-100 dark:bg-gray-900 rounded-full overflow-hidden flex">
                                    <div className="h-full bg-emerald-500 transition-all duration-1000" style={{ width: `${(s.passed_tests / (s.total_tests || 1)) * 100}%` }}></div>
                                    <div className="h-full bg-rose-500 transition-all duration-1000" style={{ width: `${(s.failed_tests / (s.total_tests || 1)) * 100}%` }}></div>
                                    <div className="h-full bg-amber-500 transition-all duration-1000" style={{ width: `${(s.error_tests / (s.total_tests || 1)) * 100}%` }}></div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <div className="text-lg font-bold">{s.total_tests}</div>
                                        <div className="text-[10px] text-gray-400 uppercase font-bold tracking-tighter">Tests Run</div>
                                    </div>
                                    <div>
                                        <div className="text-lg font-bold">{s.avg_execution_time}s</div>
                                        <div className="text-[10px] text-gray-400 uppercase font-bold tracking-tighter">Avg Speed</div>
                                    </div>
                                </div>

                                <div className="pt-2">
                                    <button className="w-full py-2 bg-gray-50 dark:bg-gray-900 group-hover:bg-primary-500 group-hover:text-white rounded-xl text-[10px] font-bold uppercase transition-colors">
                                        View Details
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
