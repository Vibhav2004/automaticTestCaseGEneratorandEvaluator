import React from 'react';
import { Globe, Search, CheckCircle2, XCircle, AlertTriangle, Clock, MousePointer2, Move, Layout } from 'lucide-react';
import { Button } from '../../components/ui';

export const WebTester = ({ url, setUrl, results, loading, onTest }) => {
    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Input Section */}
            <div className="bg-white dark:bg-gray-800 rounded-3xl p-8 border border-gray-100 dark:border-gray-700 shadow-xl shadow-gray-200/20 dark:shadow-none">
                <div className="flex flex-col md:flex-row gap-6 items-end">
                    <div className="flex-1 space-y-2 w-full">
                        <label className="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
                             <Globe className="w-3 h-3" /> Target Website URL
                        </label>
                        <div className="relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                                <Search className="w-5 h-5" />
                            </div>
                            <input 
                                type="text" 
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="https://example.com"
                                className="w-full bg-gray-50 dark:bg-gray-900/50 border border-transparent focus:border-primary-500 rounded-2xl py-4 pl-12 pr-4 outline-none transition-all text-sm font-medium"
                            />
                        </div>
                    </div>
                    <Button 
                        onClick={onTest} 
                        loading={loading} 
                        className="h-[58px] px-10 rounded-2xl shadow-lg shadow-primary-500/25"
                    >
                        {loading ? 'Testing...' : 'Start Auto-Test'}
                    </Button>
                </div>
                <p className="mt-4 text-xs text-gray-400 font-medium italic">
                    Our AI crawler will automatically scroll, find interactive elements, and verify functionality.
                </p>
            </div>

            {/* Results Section */}
            {results ? (
                <div className="grid grid-cols-12 gap-8">
                    {/* Summary Stats */}
                    <div className="col-span-12 lg:col-span-4 space-y-6">
                        <div className="bg-gradient-to-br from-indigo-600 to-primary-600 rounded-3xl p-8 text-white shadow-2xl shadow-primary-500/20">
                            <h3 className="text-xl font-bold mb-6">Execution Summary</h3>
                            <div className="space-y-4">
                                <SummaryItem 
                                    label="Total Tasks" 
                                    count={results.tasks.length} 
                                    icon={Layout} 
                                />
                                <SummaryItem 
                                    label="Passed" 
                                    count={results.tasks.filter(t => t.status === 'passed').length} 
                                    icon={CheckCircle2} 
                                    color="bg-green-400/20"
                                />
                                <SummaryItem 
                                    label="Failed" 
                                    count={results.tasks.filter(t => t.status === 'failed').length} 
                                    icon={XCircle} 
                                    color="bg-rose-400/20"
                                />
                            </div>
                            <div className="mt-8 pt-8 border-t border-white/10 text-[10px] uppercase font-bold tracking-widest opacity-60">
                                Tested at: {new Date(results.timestamp).toLocaleString()}
                            </div>
                        </div>
                    </div>

                    {/* Detailed Task Log */}
                    <div className="col-span-12 lg:col-span-8 flex flex-col gap-4">
                        {results.tasks.map((task, idx) => (
                            <TaskCard key={idx} task={task} />
                        ))}
                    </div>
                </div>
            ) : !loading && (
                <div className="flex flex-col items-center justify-center p-20 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-[3rem] text-center opacity-50">
                    <Globe className="w-16 h-16 text-gray-300 mb-4" />
                    <h4 className="text-lg font-bold">Ready to inspect</h4>
                    <p className="text-sm max-w-xs mx-auto">Enter a URL above to start the automated sanity check of your web application.</p>
                </div>
            )}
        </div>
    );
};

const SummaryItem = ({ label, count, icon: Icon, color = "bg-white/10" }) => (
    <div className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/5">
        <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${color}`}>
                <Icon className="w-4 h-4" />
            </div>
            <span className="text-xs font-bold uppercase tracking-wider">{label}</span>
        </div>
        <span className="text-2xl font-black">{count}</span>
    </div>
);

const TaskCard = ({ task }) => {
    const getIcon = (action) => {
        switch(action) {
            case 'navigation': return <Globe className="w-4 h-4" />;
            case 'scrolling': return <Move className="w-4 h-4" />;
            case 'interaction': return <MousePointer2 className="w-4 h-4" />;
            case 'seo_check': return <Search className="w-4 h-4" />;
            default: return <Layout className="w-4 h-4" />;
        }
    };

    const isPassed = task.status === 'passed';
    const isWarning = task.status === 'warning';

    return (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl border border-gray-100 dark:border-gray-700 flex items-center gap-6 group hover:shadow-lg hover:shadow-gray-200/20 dark:hover:shadow-none transition-all">
            <div className={`p-4 rounded-2xl flex-shrink-0 ${
                isPassed ? 'bg-emerald-50 text-emerald-500 dark:bg-emerald-500/10' : 
                isWarning ? 'bg-amber-50 text-amber-500 dark:bg-amber-500/10' :
                'bg-rose-50 text-rose-500 dark:bg-rose-500/10'
            }`}>
                {getIcon(task.action)}
            </div>
            
            <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">{task.action}</span>
                    <div className="w-1 h-1 rounded-full bg-gray-300"></div>
                    <h5 className="text-sm font-bold text-gray-900 dark:text-gray-100">{task.target}</h5>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 font-medium leading-relaxed">{task.message}</p>
            </div>

            <div className="flex flex-col items-end gap-2">
                <div className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter ${
                    isPassed ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-400' :
                    isWarning ? 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400' :
                    'bg-rose-100 text-rose-700 dark:bg-rose-500/20 dark:text-rose-400'
                }`}>
                    {task.status}
                </div>
                <div className="flex items-center gap-1 text-[10px] font-bold text-gray-300">
                    <Clock className="w-3 h-3" />
                    {new Date(task.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </div>
            </div>
        </div>
    );
};
