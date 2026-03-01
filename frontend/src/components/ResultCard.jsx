import React from 'react';
import { motion } from 'framer-motion';
import { Leaf, Activity, AlertTriangle, Recycle } from 'lucide-react';

const ResultCard = ({ result }) => {
    if (!result) return null;

    const { category, confidence, co2_saved_grams, eco_fact } = result;

    const categoryConfig = {
        biodegradable: {
            color: 'text-amber-600',
            bgBase: 'bg-amber-50',
            bgGlow: 'bg-amber-100',
            icon: <Leaf className="w-8 h-8 text-amber-500" />,
            title: 'Biodegradable'
        },
        recyclable: {
            color: 'text-ocean-600',
            bgBase: 'bg-ocean-50',
            bgGlow: 'bg-ocean-100',
            icon: <Recycle className="w-8 h-8 text-ocean-500" />,
            title: 'Recyclable'
        },
        hazardous: {
            color: 'text-alert-600',
            bgBase: 'bg-alert-50',
            bgGlow: 'bg-alert-100',
            icon: <AlertTriangle className="w-8 h-8 text-alert-500" />,
            title: 'Hazardous'
        }
    };

    const config = categoryConfig[category.toLowerCase()] || categoryConfig.recyclable;
    const confPercent = (confidence * 100).toFixed(1);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-panel w-full overflow-hidden"
        >
            {/* Header Banner */}
            <div className={`${config.bgGlow} p-6 flex items-center gap-4`}>
                <div className="bg-white p-3 rounded-2xl shadow-sm">
                    {config.icon}
                </div>
                <div>
                    <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">
                        Detected Category
                    </h3>
                    <div className="flex items-center gap-3">
                        <span className={`text-2xl font-bold ${config.color}`}>
                            {config.title}
                        </span>
                        <span className="bg-white px-2 py-1 rounded-md text-xs font-bold text-slate-700 shadow-sm border border-slate-100">
                            {confPercent}% Match
                        </span>
                    </div>
                </div>
            </div>

            {/* Body Content */}
            <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* CO2 Impact */}
                    <div className="bg-slate-50 rounded-xl p-5 border border-slate-100 flex flex-col justify-center">
                        <div className="flex items-center gap-2 mb-2 text-forest-600">
                            <Activity className="w-5 h-5" />
                            <h4 className="font-semibold">Environmental Impact</h4>
                        </div>
                        <div className="flex items-baseline gap-1 mt-2">
                            <span className="text-4xl font-extrabold text-slate-800">
                                +{co2_saved_grams}
                            </span>
                            <span className="text-slate-500 font-medium">grams CO₂ saved</span>
                        </div>
                        <p className="text-xs text-slate-400 mt-2">
                            By properly disposing of this item instead of landfilling.
                        </p>
                    </div>

                    {/* Eco Fact */}
                    <div className={`${config.bgBase} rounded-xl p-5 border border-white`}>
                        <h4 className={`font-semibold ${config.color} mb-2`}>Did you know?</h4>
                        <p className="text-sm text-slate-700 leading-relaxed italic">
                            "{eco_fact}"
                        </p>
                    </div>
                </div>
            </div>
        </motion.div>
    );
};

export default ResultCard;
