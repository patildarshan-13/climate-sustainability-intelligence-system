import React, { useState, useCallback } from 'react';
import { Upload, FileText } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const FileUpload = ({ onUploadComplete }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  }, []);

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
    e.target.value = ''; // Reset input after upload
  };

  const handleBrowseClick = () => {
    document.getElementById('file-input').click();
  };

  const uploadFile = async (file) => {
    const allowedTypes = ['.pdf', '.txt', '.md', '.markdown'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.some(ext => fileExt === ext)) {
      toast.error(`Unsupported file type. Allowed: PDF, TXT, Markdown`);
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API}/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      toast.success(`Document "${file.name}" uploaded and processed successfully!`);
      if (onUploadComplete) {
        onUploadComplete(response.data);
      }
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full"
    >
      <div
        data-testid="file-upload-zone"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`upload-zone glass-card rounded-2xl p-12 text-center cursor-pointer ${
          isDragging ? 'dragging' : ''
        }`}
      >
        <input
          data-testid="file-input"
          type="file"
          onChange={handleFileSelect}
          accept=".pdf,.txt,.md,.markdown"
          className="hidden"
          id="file-input"
          disabled={uploading}
        />
        <div className="cursor-pointer">
          <motion.div
            animate={{ scale: uploading ? [1, 1.1, 1] : 1 }}
            transition={{ repeat: uploading ? Infinity : 0, duration: 1.5 }}
            className="flex flex-col items-center gap-6"
          >
            <div className="w-24 h-24 rounded-full bg-[#ccff00]/10 flex items-center justify-center">
              {uploading ? (
                <div className="w-12 h-12 border-4 border-[#ccff00] border-t-transparent rounded-full animate-spin" />
              ) : (
                <Upload className="w-12 h-12 text-[#ccff00]" strokeWidth={1.5} />
              )}
            </div>

            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-white">
                {uploading ? 'Processing Document...' : 'Drop your documents here'}
              </h3>
              <p className="text-[#a1a1aa] text-base">
                Supports PDF, TXT, and Markdown files
              </p>
            </div>

            {!uploading && (
              <button
                data-testid="browse-files-btn"
                onClick={handleBrowseClick}
                type="button"
                className="bg-[#ccff00] text-black hover:bg-[#b3e600] rounded-full px-8 py-4 font-semibold tracking-tight"
              >
                Browse Files
              </button>
            )}
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};
