import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Trash2, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const DocumentCard = ({ document, onDelete }) => {
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`${API}/documents/${document.id}`);
      toast.success('Document deleted successfully');
      if (onDelete) onDelete(document.id);
    } catch (error) {
      toast.error('Failed to delete document');
    }
  };

  const getStatusIcon = () => {
    if (document.status === 'ready') return <CheckCircle className="w-5 h-5 text-[#14b8a6]" />;
    if (document.status === 'processing') return <Clock className="w-5 h-5 text-[#ccff00] animate-spin" />;
    if (document.status === 'error') return <AlertCircle className="w-5 h-5 text-red-400" />;
    return null;
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -2 }}
      data-testid={`document-card-${document.id}`}
      className="glass-card rounded-xl p-6 hover:border-[#ccff00]/30 transition-all duration-300"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex gap-4 flex-1">
          <div className="w-12 h-12 rounded-lg bg-[#ccff00]/10 flex items-center justify-center flex-shrink-0">
            <FileText className="w-6 h-6 text-[#ccff00]" strokeWidth={1.5} />
          </div>

          <div className="flex-1 min-w-0">
            <h3 className="text-base font-semibold text-white truncate mb-2">
              {document.filename}
            </h3>

            <div className="flex flex-wrap gap-3 text-sm text-[#a1a1aa]">
              <span>{formatFileSize(document.file_size)}</span>
              <span>•</span>
              <span>{document.chunk_count} chunks</span>
              <span>•</span>
              <span>{document.total_tokens.toLocaleString()} tokens</span>
            </div>

            <div className="flex items-center gap-2 mt-3">
              {getStatusIcon()}
              <span className={`text-sm ${document.status === 'error' ? 'text-red-400' : 'text-[#a1a1aa]'}`}>
                {document.status === 'ready' ? 'Ready' : document.status === 'error' ? 'Processing Failed' : 'Processing...'}
              </span>
              <span className="text-sm text-[#52525b]">•</span>
              <span className="text-sm text-[#52525b]">
                {formatDate(document.upload_date)}
              </span>
            </div>
          </div>
        </div>

        <button
          data-testid={`delete-document-btn-${document.id}`}
          onClick={handleDelete}
          className="p-2 hover:bg-white/5 rounded-lg transition-colors"
          title="Delete document"
        >
          <Trash2 className="w-5 h-5 text-[#a1a1aa] hover:text-red-400" strokeWidth={1.5} />
        </button>
      </div>
    </motion.div>
  );
};
