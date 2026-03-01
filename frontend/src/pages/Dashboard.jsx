import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Globe, Users, CloudRain } from 'lucide-react';
import { fetchAnalytics } from '../services/api';
import { CategoryPieChart } from '../components/Charts';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchAnalytics();
                setData(result.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-forest-500"></div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="w-full max-w-6xl mx-auto px-6 py-12 text-center">
                <div className="glass-panel p-8 inline-block max-w-xl">
                    <CloudRain className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                    <h2 className="text-xl font-bold text-slate-700 mb-2">No Data Available</h2>
                    <p className="text-slate-500 text-sm">Upload some images to start generating environmental impact analytics.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-6xl mx-auto px-6 py-8">
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
            >
                <h1 className="text-3xl font-extrabold text-slate-800 mb-2">Global Impact Dashboard</h1>
                <p className="text-slate-500">Aggregated telemetry from the EcoVision network.</p>
            </motion.div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="glass-panel p-6 border-l-4 border-l-forest-500 relative overflow-hidden"
                >
                    <div className="z-10 relative">
                        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Total CO₂ Prevented</h3>
                        <div className="flex items-baseline gap-2">
                            <span className="text-5xl font-extrabold text-slate-800">{data.total_co2_saved_kg}</span>
                            <span className="text-lg font-medium text-slate-500">kg</span>
                        </div>
                    </div>
                    <Globe className="absolute right-[-20px] bottom-[-20px] w-32 h-32 text-forest-50 opacity-50 z-0" />
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="glass-panel p-6 border-l-4 border-l-ocean-500 relative overflow-hidden"
                >
                    <div className="z-10 relative">
                        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Items Scanned</h3>
                        <div className="flex items-baseline gap-2">
                            <span className="text-5xl font-extrabold text-slate-800">{data.total_scans}</span>
                            <span className="text-lg font-medium text-slate-500">items</span>
                        </div>
                    </div>
                    <Users className="absolute right-[-20px] bottom-[-20px] w-32 h-32 text-ocean-50 opacity-50 z-0" />
                </motion.div>
            </div>

            {/* Charts Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass-panel p-6"
            >
                <h3 className="text-lg font-bold text-slate-800 mb-6">Waste Distribution</h3>
                <CategoryPieChart data={data.breakdown} />
            </motion.div>
        </div>
    );
};

export default Dashboard;
