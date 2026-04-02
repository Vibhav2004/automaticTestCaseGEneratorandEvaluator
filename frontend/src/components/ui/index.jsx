import React from 'react';

export const StatCard = ({ label, value, color, icon: Icon }) => (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow">
        <div className="flex justify-between items-start mb-2">
            <p className="text-[10px] font-bold uppercase tracking-wider text-gray-400">{label}</p>
            {Icon && <Icon className={`w-4 h-4 ${color}`} />}
        </div>
        <h2 className={`text-2xl font-bold ${color}`}>{value}</h2>
    </div>
);

export const Button = ({ children, onClick, disabled, className = "", variant = "primary", icon: Icon }) => {
    const variants = {
        primary: "bg-primary-600 hover:bg-primary-700 text-white shadow-primary-500/25",
        secondary: "bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100",
        danger: "bg-rose-500 hover:bg-rose-600 text-white shadow-rose-500/25"
    };

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`px-6 py-2 rounded-xl text-sm font-semibold transition-all flex items-center gap-2 shadow-lg disabled:bg-gray-400 disabled:shadow-none ${variants[variant]} ${className}`}
        >
            {Icon && <Icon className="w-4 h-4" />}
            {children}
        </button>
    );
};
