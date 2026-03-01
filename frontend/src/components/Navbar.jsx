import React from 'react';
import { NavLink } from 'react-router-dom';
import { Leaf, UploadCloud, BarChart3 } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="sticky top-0 z-50 w-full glass-panel border-x-0 border-t-0 rounded-none shadow-sm px-6 py-4 mb-8">
            <div className="max-w-6xl mx-auto flex justify-between items-center bg-transparent">
                <NavLink to="/" className="flex items-center gap-2 group">
                    <div className="p-2 bg-gradient-to-br from-forest-500 to-ocean-500 rounded-xl shadow-md group-hover:shadow-lg transition-all duration-300">
                        <Leaf className="w-5 h-5 text-white" />
                    </div>
                    <span className="font-bold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-forest-900 to-ocean-600">
                        EcoVision
                    </span>
                </NavLink>

                <div className="flex items-center gap-1 sm:gap-4 bg-transparent">
                    <NavLink
                        to="/"
                        className={({ isActive }) => `px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-forest-100 text-forest-900' : 'text-slate-600 hover:bg-slate-100'}`}
                    >
                        <span className="hidden sm:inline">Home</span>
                        <Leaf className="w-5 h-5 sm:hidden" />
                    </NavLink>
                    <NavLink
                        to="/upload"
                        className={({ isActive }) => `px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-forest-100 text-forest-900' : 'text-slate-600 hover:bg-slate-100'}`}
                    >
                        <span className="hidden sm:inline">Analyze</span>
                        <UploadCloud className="w-5 h-5 sm:hidden" />
                    </NavLink>
                    <NavLink
                        to="/dashboard"
                        className={({ isActive }) => `px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-forest-100 text-forest-900' : 'text-slate-600 hover:bg-slate-100'}`}
                    >
                        <span className="hidden sm:inline">Impact</span>
                        <BarChart3 className="w-5 h-5 sm:hidden" />
                    </NavLink>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
