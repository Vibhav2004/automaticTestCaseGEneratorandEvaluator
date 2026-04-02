import React from 'react';
import { Code2, ShieldCheck } from 'lucide-react';

export const EditorSection = ({ code, setCode, functions }) => {
    return (
        <div className="flex flex-col gap-8 h-full">
            <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col flex-1">
                <div className="flex justify-between items-center mb-4">
                    <span className="text-sm font-bold flex items-center gap-2">
                        <Code2 className="w-4 h-4 text-primary-500" /> Source Code
                    </span>
                    <span className="text-[10px] text-gray-400 font-mono">Polyglot Mode Active</span>
                </div>
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    className="flex-1 bg-gray-50 dark:bg-gray-900 p-4 rounded-2xl font-mono text-sm border-none focus:ring-1 focus:ring-primary-500 resize-none overflow-auto scrollbar-hide"
                    spellCheck="false"
                    placeholder="Paste your code here..."
                />
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <h3 className="text-sm font-bold mb-4 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-500" />
                    Foundations: {functions.length} Functions
                </h3>
                <div className="space-y-3 max-h-[200px] overflow-y-auto pr-2">
                    {functions.length === 0 ? (
                        <p className="text-xs text-gray-400 italic text-center py-4">Hit 'Analyze' to discover entry points</p>
                    ) : (
                        functions.map((fn, idx) => (
                            <div key={idx} className="p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl flex justify-between items-center group hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-colors border border-transparent hover:border-primary-100 dark:hover:border-primary-900/30">
                                <div>
                                    <span className="text-primary-500 font-mono font-bold text-sm">{fn.name}</span>
                                    <div className="flex flex-wrap gap-2 mt-1">
                                        {fn.parameters.map((p, pidx) => (
                                            <span key={pidx} className="px-2 py-0.5 bg-white dark:bg-gray-800 rounded-md text-[10px] text-gray-400 font-mono border border-gray-100 dark:border-gray-700">
                                                {p.name}: {p.type_hint}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <span className="text-[10px] text-gray-400 font-medium">L{fn.line_number}</span>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};
