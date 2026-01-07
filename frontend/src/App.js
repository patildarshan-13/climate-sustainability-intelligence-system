import React, { useState, useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Leaf, Upload, MessageSquare, Database, BarChart3 } from 'lucide-react';
import axios from 'axios';
import { Toaster } from 'sonner';

import { FileUpload } from './components/FileUpload';
import { DocumentCard } from './components/DocumentCard';
import { QueryInterface } from './components/QueryInterface';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Home Page
const HomePage = () => {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div className="min-h-screen bg-[#050505] noise-texture">
      {/* Hero Section */}
      <div className="hero-glow min-h-screen flex flex-col">
        {/* Navigation */}
        <nav className="glass-card-heavy border-b border-white/10">
          <div className="max-w-7xl mx-auto px-8 py-6">
            <div className="flex items-center justify-between">
              <Link to="/" className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-[#ccff00] flex items-center justify-center">
                  <Leaf className="w-6 h-6 text-black" strokeWidth={2.5} />
                </div>
                <span className="text-2xl font-bold tracking-tight text-white" style={{ fontFamily: 'Outfit' }}>
                  EcoIntel
                </span>
              </Link>

              <Link to="/dashboard">
                <button
                  data-testid="start-querying-btn"
                  className="bg-[#ccff00] text-black hover:bg-[#b3e600] rounded-full px-8 py-3 font-semibold tracking-tight"
                >
                  Start Querying
                </button>
              </Link>
            </div>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="flex-1 flex items-center">
          <div className="max-w-7xl mx-auto px-8 py-24">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left Side */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                className="space-y-8"
              >
                <div className="inline-block">
                  <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#ccff00]/10 border border-[#ccff00]/20 text-[#ccff00] text-sm font-semibold uppercase tracking-widest">
                    <Leaf className="w-4 h-4" />
                    AI-Powered Document Intelligence
                  </span>
                </div>

                <h1
                  className="text-5xl lg:text-6xl font-light leading-tight text-white"
                  style={{ fontFamily: 'Outfit' }}
                >
                  Climate &<br />
                  <span className="font-semibold">Sustainability</span><br />
                  <span className="gradient-text font-semibold">Intelligence</span>
                </h1>

                <p className="text-lg text-[#a1a1aa] leading-relaxed max-w-xl">
                  Upload ESG disclosures, carbon reports, and policy documents. Ask questions in natural language and get accurate, context-aware insights powered by RAG.
                </p>

                <button
                  data-testid="upload-document-btn"
                  onClick={() => setShowUpload(!showUpload)}
                  className="bg-[#ccff00] text-black hover:bg-[#b3e600] rounded-full px-12 py-6 font-semibold tracking-tight text-lg inline-flex items-center gap-3"
                >
                  <Upload className="w-5 h-5" strokeWidth={2} />
                  Upload Document
                </button>
              </motion.div>

              {/* Right Side - Upload or Feature Cards */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                {showUpload ? (
                  <FileUpload onUploadComplete={() => setShowUpload(false)} />
                ) : (
                  <div className="space-y-6">
                    {/* Feature Cards */}
                    <div className="glass-card rounded-2xl p-8 hover:border-[#ccff00]/30 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="w-14 h-14 rounded-xl bg-[#ccff00]/10 flex items-center justify-center flex-shrink-0">
                          <Database className="w-7 h-7 text-[#ccff00]" strokeWidth={1.5} />
                        </div>
                        <div>
                          <h3 className="text-xl font-semibold text-white mb-2">Document Intelligence</h3>
                          <p className="text-[#a1a1aa] leading-relaxed">
                            Upload ESG disclosures, carbon reports, and policy documents for analysis.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="glass-card rounded-2xl p-8 hover:border-[#ccff00]/30 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="w-14 h-14 rounded-xl bg-[#14b8a6]/10 flex items-center justify-center flex-shrink-0">
                          <MessageSquare className="w-7 h-7 text-[#14b8a6]" strokeWidth={1.5} />
                        </div>
                        <div>
                          <h3 className="text-xl font-semibold text-white mb-2">RAG-Powered Answers</h3>
                          <p className="text-[#a1a1aa] leading-relaxed">
                            Get accurate, context-aware responses grounded in your documents.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="glass-card rounded-2xl p-8 hover:border-[#ccff00]/30 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="w-14 h-14 rounded-xl bg-[#0ea5e9]/10 flex items-center justify-center flex-shrink-0">
                          <BarChart3 className="w-7 h-7 text-[#0ea5e9]" strokeWidth={1.5} />
                        </div>
                        <div>
                          <h3 className="text-xl font-semibold text-white mb-2">Source References</h3>
                          <p className="text-[#a1a1aa] leading-relaxed">
                            Every answer includes references to the source document sections.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard Page
const DashboardPage = () => {
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('documents');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDocuments();
    fetchStats();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API}/documents`);
      setDocuments(response.data);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleUploadComplete = (newDoc) => {
    setDocuments(prev => [newDoc, ...prev]);
    fetchStats();
  };

  const handleDeleteDocument = (docId) => {
    setDocuments(prev => prev.filter(doc => doc.id !== docId));
    fetchStats();
  };

  return (
    <div className="min-h-screen bg-[#050505] noise-texture">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-screen w-64 glass-card-heavy border-r border-white/10 z-10">
        <div className="p-8">
          <Link to="/" className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 rounded-full bg-[#ccff00] flex items-center justify-center">
              <Leaf className="w-5 h-5 text-black" strokeWidth={2.5} />
            </div>
            <span className="text-xl font-bold tracking-tight text-white" style={{ fontFamily: 'Outfit' }}>
              EcoIntel
            </span>
          </Link>

          <nav className="space-y-2">
            <button
              data-testid="tab-documents"
              onClick={() => setActiveTab('documents')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'documents'
                  ? 'bg-[#ccff00]/10 text-[#ccff00] border-l-4 border-[#ccff00]'
                  : 'text-[#a1a1aa] hover:bg-white/5'
              }`}
            >
              <Database className="w-5 h-5" strokeWidth={1.5} />
              <span className="font-medium">Document Library</span>
            </button>

            <button
              data-testid="tab-query"
              onClick={() => setActiveTab('query')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'query'
                  ? 'bg-[#ccff00]/10 text-[#ccff00] border-l-4 border-[#ccff00]'
                  : 'text-[#a1a1aa] hover:bg-white/5'
              }`}
            >
              <MessageSquare className="w-5 h-5" strokeWidth={1.5} />
              <span className="font-medium">Query Interface</span>
            </button>
          </nav>

          {/* Stats */}
          {stats && (
            <div className="mt-12 space-y-4">
              <div className="glass-card rounded-xl p-4">
                <div className="text-3xl font-bold text-[#ccff00]" style={{ fontFamily: 'Outfit' }}>
                  {stats.ready_documents}
                </div>
                <div className="text-sm text-[#a1a1aa]">Ready Documents</div>
              </div>

              <div className="glass-card rounded-xl p-4">
                <div className="text-3xl font-bold text-[#14b8a6]" style={{ fontFamily: 'Outfit' }}>
                  {stats.total_queries}
                </div>
                <div className="text-sm text-[#a1a1aa]">Total Queries</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-12">
        {activeTab === 'documents' && (
          <div data-testid="documents-tab" className="space-y-8">
            <div>
              <h1 className="text-4xl font-semibold text-white mb-2" style={{ fontFamily: 'Outfit' }}>
                Document Library
              </h1>
              <p className="text-[#a1a1aa]">{documents.length} documents uploaded</p>
            </div>

            <FileUpload onUploadComplete={handleUploadComplete} />

            <div className="space-y-4">
              {loading ? (
                <div className="text-center py-12">
                  <div className="w-12 h-12 border-4 border-[#ccff00] border-t-transparent rounded-full animate-spin mx-auto" />
                </div>
              ) : documents.length === 0 ? (
                <div className="glass-card rounded-2xl p-12 text-center">
                  <Database className="w-16 h-16 text-[#52525b] mx-auto mb-4" strokeWidth={1.5} />
                  <h3 className="text-xl font-semibold text-white mb-2">No documents yet</h3>
                  <p className="text-[#a1a1aa]">
                    Upload your first sustainability or climate-related document to start querying.
                  </p>
                </div>
              ) : (
                documents.map(doc => (
                  <DocumentCard key={doc.id} document={doc} onDelete={handleDeleteDocument} />
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'query' && (
          <div data-testid="query-tab" className="h-[calc(100vh-6rem)]">
            <div className="h-full glass-card rounded-2xl overflow-hidden flex flex-col">
              <div className="p-6 border-b border-white/10">
                <h1 className="text-3xl font-semibold text-white" style={{ fontFamily: 'Outfit' }}>
                  Query Interface
                </h1>
                <p className="text-[#a1a1aa] mt-1">
                  Ask questions about your uploaded documents
                </p>
              </div>
              <QueryInterface documentCount={documents.filter(d => d.status === 'ready').length} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <Toaster position="top-right" theme="dark" />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
