import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2, Scale, Leaf } from 'lucide-react';
import UploadZone from '../components/UploadZone';
import ResultCard from '../components/ResultCard';
import { predictWaste } from '../services/api';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [weight, setWeight] = useState(100);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const handleAnalyze = async () => {
        if (!file) return;

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const data = await predictWaste(file, weight);
            setResult(data);
        } catch (err) {
            setError(err.message || 'An error occurred during analysis.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto px-6 py-8">
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
            >
                <h1 className="text-3xl font-extrabold text-slate-800 mb-2">Analyze Waste</h1>
                <p className="text-slate-500">Upload a clear photo of the item you want to dispose of.</p>
            </motion.div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Left Column: Input */}
                <div className="space-y-6">
                    <UploadZone file={file} setFile={setFile} />

                    {/* Weight Input */}
                    <div className="glass-panel p-5">
                        <label className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-3">
                            <Scale className="w-4 h-4 text-slate-400" />
                            Estimated Weight (grams)
                        </label>
                        <div className="flex items-center gap-3">
                            <input
                                type="range"
                                min="10"
                                max="2000"
                                step="10"
                                value={weight}
                                onChange={(e) => setWeight(e.target.value)}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-forest-500"
                            />
                            <div className="bg-slate-100 px-3 py-1.5 rounded-md border border-slate-200 min-w-[80px] text-center font-mono text-sm font-medium text-slate-700 shadow-inner">
                                {weight}g
                            </div>
                        </div>
                    </div>

                    {/* Action Button */}
                    <button
                        onClick={handleAnalyze}
                        disabled={!file || loading}
                        className={`w-full py-4 rounded-xl font-bold text-white shadow-lg transition-all flex items-center justify-center gap-2
              ${!file || loading
                                ? 'bg-slate-300 cursor-not-allowed shadow-none'
                                : 'bg-forest-600 hover:bg-forest-700 hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0'
                            }`}
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" />
                                Analyzing with AI...
                            </>
                        ) : (
                            'Scan & Analyze Impact'
                        )}
                    </button>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 text-sm font-medium"
                        >
                            {error}
                        </motion.div>
                    )}
                </div>

                {/* Right Column: Output */}
                <div className="flex flex-col h-full">
                    {result ? (
                        <ResultCard result={result} />
                    ) : (
                        <div className="glass-panel h-full min-h-[400px] flex items-center justify-center border-dashed border-2 bg-slate-50/50">
                            <div className="text-center p-6">
                                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-200">
                                    <Leaf className="w-8 h-8 text-slate-300" />
                                </div>
                                <h3 className="text-slate-500 font-medium">Your results will appear here</h3>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Upload;
