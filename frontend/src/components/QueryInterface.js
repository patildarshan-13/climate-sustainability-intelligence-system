import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles, FileText } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const QueryInterface = ({ documentCount }) => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    if (documentCount === 0) {
      toast.error('Please upload documents before querying');
      return;
    }

    const currentQuestion = question.trim();
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: currentQuestion,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/query`, {
        question: currentQuestion,
        top_k: 5
      });

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Query error:', error);
      toast.error('Failed to process query');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div data-testid="query-interface" className="flex flex-col h-full">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-6 p-6">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`query-message flex gap-4 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.type === 'ai' && (
                <div className="w-10 h-10 rounded-full bg-[#ccff00]/10 flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-5 h-5 text-[#ccff00]" strokeWidth={1.5} />
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-4 ${
                  message.type === 'user'
                    ? 'bg-[#ccff00]/10 border border-[#ccff00]/20'
                    : 'glass-card'
                }`}
              >
                <p className="text-base text-white leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>

                {message.sources && message.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm font-semibold text-[#ccff00] mb-2">Sources:</p>
                    <div className="space-y-2">
                      {message.sources.map((source, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 text-sm text-[#a1a1aa]"
                        >
                          <FileText className="w-4 h-4" strokeWidth={1.5} />
                          <span>{source.filename} (Chunk {source.chunk_index})</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-2 text-xs text-[#52525b]">
                  {message.timestamp.toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-4"
          >
            <div className="w-10 h-10 rounded-full bg-[#ccff00]/10 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-[#ccff00]" strokeWidth={1.5} />
            </div>
            <div className="glass-card rounded-2xl p-4">
              <div className="flex gap-2">
                <span className="w-2 h-2 bg-[#ccff00] rounded-full pulse-dot" />
                <span className="w-2 h-2 bg-[#ccff00] rounded-full pulse-dot" style={{ animationDelay: '0.2s' }} />
                <span className="w-2 h-2 bg-[#ccff00] rounded-full pulse-dot" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-6 border-t border-white/10">
        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            data-testid="query-input"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your documents..."
            disabled={loading}
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-6 py-4 text-white placeholder:text-white/30 focus:border-[#ccff00]/50 focus:ring-1 focus:ring-[#ccff00]/50 transition-all outline-none"
          />
          <button
            data-testid="send-query-btn"
            type="submit"
            disabled={loading || !question.trim()}
            className="bg-[#ccff00] text-black hover:bg-[#b3e600] rounded-xl px-8 py-4 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" strokeWidth={2} />
          </button>
        </form>
      </div>
    </div>
  );
};
