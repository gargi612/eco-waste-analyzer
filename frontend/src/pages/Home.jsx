import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Leaf, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="w-full max-w-6xl mx-auto px-6 py-12">
            {/* Hero Section */}
            <div className="flex flex-col items-center text-center mt-10 mb-20 relative">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-forest-100 text-forest-800 font-medium text-sm mb-6 shadow-sm border border-forest-200"
                >
                    <Leaf className="w-4 h-4" />
                    <span>Powered by PyTorch MobileNetV2</span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1, duration: 0.5 }}
                    className="text-5xl sm:text-7xl font-extrabold text-slate-800 tracking-tight leading-tight mb-6"
                >
                    Segregate Waste.<br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-forest-500 to-ocean-500">
                        Save the Planet.
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                    className="text-lg sm:text-xl text-slate-500 max-w-2xl mb-10"
                >
                    Instantly classify your waste using AI and calculate exactly how much
                    CO₂ emissions you prevent from entering the atmosphere.
                </motion.p>

                <motion.button
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                    onClick={() => navigate('/upload')}
                    className="group relative inline-flex items-center justify-center gap-2 px-8 py-4 font-bold text-white bg-slate-900 rounded-full overflow-hidden transition-all hover:scale-105 shadow-xl hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-slate-300"
                >
                    <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-forest-500 to-ocean-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                    <span className="relative z-10">Start Analyzing Now</span>
                    <ArrowRight className="relative z-10 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
                <FeatureCard
                    icon={<Zap className="w-6 h-6 text-amber-500" />}
                    title="Instant AI Detection"
                    desc="Take a picture and let our advanced neural network classify it instantly with high accuracy."
                />
                <FeatureCard
                    icon={<Leaf className="w-6 h-6 text-forest-500" />}
                    title="Live Carbon Tracking"
                    desc="See exactly how many grams of CO₂ you save with every item properly disposed of."
                />
                <FeatureCard
                    icon={<ShieldCheck className="w-6 h-6 text-ocean-500" />}
                    title="Hazardous Security"
                    desc="Safely identify hazardous materials like batteries before they contaminate recycling chains."
                />
            </div>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <motion.div
        whileHover={{ y: -5 }}
        className="glass-panel p-6"
    >
        <div className="w-12 h-12 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center mb-4 shadow-sm">
            {icon}
        </div>
        <h3 className="text-lg font-bold text-slate-800 mb-2">{title}</h3>
        <p className="text-slate-500 leading-relaxed text-sm">{desc}</p>
    </motion.div>
);

export default Home;
