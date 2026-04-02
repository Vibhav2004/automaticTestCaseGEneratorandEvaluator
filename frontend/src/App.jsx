import React, { useState, useEffect } from 'react';
import {
    Terminal, Code2, Play, Settings, BarChart3,
    History, Sun, Moon, Cpu, RotateCcw, Zap, Upload, Globe
} from 'lucide-react';

// UI Components
import { Button } from './components/ui';

// Features
import { EditorSection } from './features/editor/EditorSection';
import { AnalyticsDashboard } from './features/analytics/AnalyticsDashboard';
import { HistorySection } from './features/history/HistorySection';
import { ApiTester } from './features/api_tester/ApiTester';
import { WebTester } from './features/web_tester/WebTester';

// Hooks
import { useAutoTest } from './hooks/useAutoTest';

function App() {
    const {
        code, setCode,
        language, setLanguage,
        functions, testCases,
        results, setResults,
        loading, error, setError,
        sessions, setSessions,
        webUrl, setWebUrl,
        webResults, setWebResults,
        handleAnalyze, handleExecute, handleFileUpload, handleWebTest
    } = useAutoTest();

    const [view, setView] = useState('editor'); // editor | sessions | api_tester | web_tester
    const [darkMode, setDarkMode] = useState(true);

    useEffect(() => {
        if (darkMode) document.documentElement.classList.add('dark');
        else document.documentElement.classList.remove('dark');
    }, [darkMode]);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans transition-colors duration-300">
            {/* Ultra-Modern Navigation Sidebar */}
            <aside className="fixed left-0 top-0 h-full w-20 flex flex-col items-center py-8 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 z-30">
                <div className="p-3 bg-primary-600 rounded-2xl mb-12 shadow-xl shadow-primary-500/30 group cursor-pointer hover:rotate-12 transition-transform">
                    <Cpu className="w-8 h-8 text-white" />
                </div>

                <nav className="flex flex-col gap-8 flex-1">
                    <NavIcon icon={Code2} active={view === 'editor'} onClick={() => setView('editor')} label="Code Tester" />
                    <NavIcon icon={Globe} active={view === 'web_tester'} onClick={() => setView('web_tester')} label="Web Tester" />
                    <NavIcon icon={Terminal} active={view === 'api_tester'} onClick={() => setView('api_tester')} label="API Tester" />
                    <NavIcon icon={History} active={view === 'sessions'} onClick={() => setView('sessions')} label="History" />
                    <NavIcon icon={BarChart3} active={false} label="Analytics" disabled />
                    <NavIcon icon={Settings} active={false} label="Settings" disabled />
                </nav>

                <button
                    onClick={() => setDarkMode(!darkMode)}
                    className="p-3 mt-auto text-gray-400 transition-all hover:text-amber-500 hover:scale-110"
                >
                    {darkMode ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
                </button>
            </aside>

            {/* Main Application Area */}
            <main className="pl-20 min-h-screen">
                {/* Header with Glassmorphism */}
                <header className="px-8 py-6 flex justify-between items-center border-b border-gray-200 dark:border-gray-700 bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl sticky top-0 z-20">
                    <div className="animate-in slide-in-from-left duration-500">
                        <h1 className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-primary-500 to-indigo-500 tracking-tight">
                            AutoTestAI <span className="text-xs font-bold text-gray-400 align-top ml-1">v2.0</span>
                        </h1>
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Enterprise Polyglot Engine</p>
                    </div>

                    <div className="flex gap-4 items-center">
                        {view === 'editor' && (
                            <>
                                <LanguageSelector value={language} onChange={setLanguage} />
                                <div className="hidden md:flex gap-3">
                                    <input type="file" onChange={handleFileUpload} accept=".py,.java,.js,.cpp,.cs,.go" className="hidden" id="file-upload" />
                                    <label htmlFor="file-upload" className="px-5 py-2.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-2xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 border border-transparent hover:border-gray-300 dark:hover:border-gray-500 shadow-sm">
                                        <Upload className="w-4 h-4 text-primary-500" /> Upload
                                    </label>

                                    <Button onClick={handleAnalyze} disabled={loading} variant="secondary" icon={Zap}>
                                        Analyze
                                    </Button>

                                    <Button onClick={handleExecute} disabled={loading || testCases.length === 0} icon={Play}>
                                        {loading ? 'Running...' : 'Run Tests'}
                                    </Button>
                                </div>
                            </>
                        )}
                        
                        {view === 'web_tester' && (
                            <div className="px-4 py-2 bg-primary-50 dark:bg-primary-900/10 rounded-2xl border border-primary-100 dark:border-primary-900/30">
                                <span className="text-[10px] font-black uppercase tracking-widest text-primary-600 dark:text-primary-400">Mode: </span>
                                <span className="text-[10px] font-black uppercase tracking-widest text-primary-700 dark:text-primary-200">Website Automation</span>
                            </div>
                        )}
                    </div>
                </header>

                {/* Error Banner */}
                {error && (
                    <div className="mx-8 mt-6 p-4 bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-900/40 rounded-2xl flex items-center justify-between text-rose-600 dark:text-rose-400 animate-in zoom-in duration-300">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-rose-100 dark:bg-rose-900/30 rounded-lg">
                                <Zap className="w-4 h-4 text-rose-500" />
                            </div>
                            <span className="text-sm font-semibold">{error}</span>
                        </div>
                        <button onClick={() => setError(null)} className="p-2 hover:bg-rose-100 dark:hover:bg-rose-800/30 rounded-xl transition-colors">
                            <RotateCcw className="w-4 h-4" />
                        </button>
                    </div>
                )}

                {/* Content Sections */}
                <section className="p-8">
                    {view === 'editor' ? (
                        <div className="grid grid-cols-12 gap-8 min-h-[calc(100vh-180px)]">
                            <div className="col-span-12 lg:col-span-6">
                                <EditorSection code={code} setCode={setCode} functions={functions} />
                            </div>
                            <div className="col-span-12 lg:col-span-6">
                                {results ? (
                                    <AnalyticsDashboard results={results} />
                                ) : testCases.length > 0 ? (
                                    <TestsReadyState count={testCases.length} params={functions[0]?.parameters?.length || 0} />
                                ) : (
                                    <IdleState />
                                )}
                            </div>
                        </div>
                    ) : view === 'api_tester' ? (
                        <ApiTester />
                    ) : view === 'web_tester' ? (
                        <WebTester 
                            url={webUrl} 
                            setUrl={setWebUrl} 
                            results={webResults} 
                            loading={loading} 
                            onTest={handleWebTest} 
                        />
                    ) : (
                        <HistorySection sessions={sessions} setSessions={setSessions} onSelectSession={(s) => { setView('editor'); setResults(s); }} />
                    )}
                </section>
            </main>
        </div>
    );
}

// Sub-components for cleaner structure
const NavIcon = ({ icon: Icon, active, onClick, label, disabled }) => (
    <div className="relative group">
        <button
            onClick={onClick}
            disabled={disabled}
            className={`p-3.5 rounded-2xl transition-all duration-300 ${disabled ? 'opacity-20 cursor-not-allowed' : active ? 'text-primary-500 bg-primary-50 dark:bg-primary-500/10 shadow-inner' : 'text-gray-400 hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700/50'}`}
        >
            <Icon className="w-6 h-6" />
        </button>
        <span className="absolute left-full ml-4 px-2 py-1 bg-gray-900 text-white text-[10px] font-bold rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
            {label}
        </span>
    </div>
);

const LanguageSelector = ({ value, onChange }) => (
    <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-white dark:bg-gray-800 px-4 py-2.5 rounded-2xl text-xs font-bold border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-primary-500 outline-none transition-all shadow-sm"
    >
        <option value="python">Python</option>
        <option value="java">Java</option>
        <option value="javascript">JavaScript</option>
        <option value="cpp">C++</option>
        <option value="csharp">C#</option>
        <option value="go">Go</option>
    </select>
);

const TestsReadyState = ({ count, params }) => (
    <div className="h-full flex flex-col gap-6 animate-in fade-in zoom-in duration-700">
        <div className="bg-gradient-to-br from-primary-600 to-indigo-600 rounded-3xl p-10 text-white shadow-2xl shadow-primary-500/20 text-center relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-10 rotate-12">
                <Zap className="w-32 h-32" />
            </div>
            <div className="relative z-10">
                <div className="p-4 bg-white/20 rounded-full w-fit mx-auto mb-6 backdrop-blur-md">
                    <Zap className="w-10 h-10 text-white animate-pulse" />
                </div>
                <h3 className="text-2xl font-black mb-2">{count} Smart Tests Generated!</h3>
                <p className="text-primary-100 text-sm mb-8 max-w-sm mx-auto opacity-80">Our polyglot engine has completed the AST analysis and mapped all security boundaries.</p>
                <div className="flex justify-center gap-6">
                    <div className="text-center">
                        <span className="text-3xl font-black block">{params}</span>
                        <span className="text-[10px] uppercase font-bold opacity-60">Parameters</span>
                    </div>
                    <div className="w-px h-10 bg-white/20 self-center"></div>
                    <div className="text-center">
                        <span className="text-3xl font-black block">6+</span>
                        <span className="text-[10px] uppercase font-bold opacity-60">Strategies</span>
                    </div>
                </div>
            </div>
        </div>
        <div className="flex-1 bg-white dark:bg-gray-800 rounded-3xl p-8 border border-gray-100 dark:border-gray-700 flex flex-col items-center justify-center text-center">
            <Play className="w-12 h-12 text-gray-200 mb-4" />
            <p className="text-sm text-gray-400 font-medium italic">Hit "Run Tests" to execute in the secure sandbox</p>
        </div>
    </div>
);

const IdleState = () => (
    <div className="h-full flex flex-col items-center justify-center bg-white dark:bg-gray-800 rounded-[3rem] border-2 border-dashed border-gray-200 dark:border-gray-700 p-12 text-center group transition-colors hover:border-primary-300">
        <div className="p-8 bg-gray-50 dark:bg-gray-900 rounded-full mb-8 text-gray-200 group-hover:text-primary-200 transition-colors shadow-inner">
            <Zap className="w-16 h-16" />
        </div>
        <h3 className="text-2xl font-black mb-3">Enterprise Test Engine</h3>
        <p className="text-gray-500 max-w-xs mx-auto text-sm leading-relaxed">Paste your logic on the left. Our system will automatically discover boundaries, path branches, and security risks.</p>
    </div>
);

export default App;
