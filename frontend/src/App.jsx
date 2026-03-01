import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col items-center">
        <Navbar />
        <main className="flex-grow w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>

        {/* Simple Footer */}
        <footer className="w-full py-8 text-center text-slate-400 text-sm mt-auto border-t border-slate-200 bg-slate-50 relative z-10">
          <p>© {new Date().getFullYear()} EcoVision. AI-Based Waste Segregation & Carbon Footprint Analyzer.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
