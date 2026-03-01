import React, { useCallback, useState } from 'react';
import { UploadCloud, FileImage, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const UploadZone = ({ file, setFile }) => {
    const [isDragActive, setIsDragActive] = useState(false);

    const handleDragEnter = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile.type.startsWith('image/')) {
                setFile(droppedFile);
            } else {
                alert("Please upload an image file.");
            }
        }
    }, [setFile]);

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const removeFile = (e) => {
        e.stopPropagation();
        setFile(null);
    };

    return (
        <div
            className={`relative w-full h-64 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-6 transition-all duration-300 cursor-pointer overflow-hidden
        ${isDragActive ? 'border-ocean-500 bg-ocean-50' : 'border-slate-300 hover:border-forest-400 bg-slate-50 hover:bg-forest-50/50'}`}
            onDragEnter={handleDragEnter}
            onDragOver={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload').click()}
        >
            <input
                id="file-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleChange}
            />

            <AnimatePresence mode="wait">
                {!file ? (
                    <motion.div
                        key="empty"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="flex flex-col items-center text-center"
                    >
                        <div className="bg-white p-4 rounded-full shadow-sm mb-4">
                            <UploadCloud className="w-10 h-10 text-slate-400" />
                        </div>
                        <p className="font-semibold text-slate-700 text-lg mb-1">
                            Click to upload or drag and drop
                        </p>
                        <p className="text-sm text-slate-500">
                            JPG, PNG, or WEBP (Max 5MB)
                        </p>
                    </motion.div>
                ) : (
                    <motion.div
                        key="filled"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="flex flex-col items-center w-full"
                    >
                        <div className="relative w-32 h-32 mb-4 rounded-xl overflow-hidden shadow-md group">
                            <img
                                src={URL.createObjectURL(file)}
                                alt="Upload preview"
                                className="w-full h-full object-cover"
                            />
                            <div
                                className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
                                onClick={removeFile}
                            >
                                <button className="bg-white/20 hover:bg-red-500 p-2 rounded-full backdrop-blur-sm text-white transition-colors">
                                    <X className="w-5 h-5" />
                                </button>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 text-forest-700 bg-forest-100 px-4 py-2 rounded-lg">
                            <FileImage className="w-4 h-4" />
                            <span className="font-medium text-sm truncate max-w-[200px]">
                                {file.name}
                            </span>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default UploadZone;
