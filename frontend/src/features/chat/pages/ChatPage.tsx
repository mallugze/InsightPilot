import React, { useEffect, useState, useRef } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { apiFetch } from '../../../services/api';
import { 
  MessageSquareCode, 
  Send, 
  Plus, 
  Trash2, 
  Brain, 
  AlertCircle, 
  FileSpreadsheet, 
  BookOpen, 
  Sparkles,
  ExternalLink,
  Loader2,
  Clock
} from 'lucide-react';
import { Button } from '../../../components/ui/Button';

interface Message {
  id: string | number;
  role: 'user' | 'model' | 'system';
  content: string;
  timestamp: string;
  // Sprint 10B structured additions
  key_findings?: string[];
  recommendations?: string[];
  reasoning_summary?: string;
  citations?: any[];
  confidence?: {
    score: number;
    validation_success: boolean;
    citation_coverage_pct: number;
    context_completeness_pct: number;
    validation_factors: string[];
  };
  metadata?: {
    provider: string;
    cache_status: string;
    validation_status: string;
    processing_time: number;
    fallback_triggered?: boolean;
  };
}

interface ConversationSummary {
  conversation_id: string;
  workspace_id?: number;
  analysis_id?: number;
  created_at: string;
  updated_at: string;
  title: string;
}

export default function ChatPage() {
  const { uploadState } = useWorkspace();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // States
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Thinking Animation Stage Cycle
  const [thinkingIndex, setThinkingIndex] = useState(0);
  const thinkingStages = [
    "Analyzing business context...",
    "Reviewing KPIs...",
    "Checking trends...",
    "Preparing executive insights...",
  ];

  const analysisId = uploadState?.datasetId ? parseInt(uploadState.datasetId) : null;

  // 1. Initial Load & Fetch suggestions
  useEffect(() => {
    fetchConversations();
    if (analysisId) {
      fetchSuggestions();
    }
  }, [analysisId]);

  // Scroll to bottom on message updates
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isGenerating]);

  // Stage Cycle Timer during loading
  useEffect(() => {
    let interval: any;
    if (isGenerating) {
      interval = setInterval(() => {
        setThinkingIndex((prev) => (prev + 1) % thinkingStages.length);
      }, 2500);
    }
    return () => clearInterval(interval);
  }, [isGenerating]);

  const fetchConversations = async () => {
    try {
      const res = await apiFetch<any>('/v1/ai/conversations');
      if (res && res.conversations) {
        setConversations(res.conversations);
      }
    } catch (e) {
      console.error("Failed to load conversations:", e);
    }
  };

  const fetchSuggestions = async () => {
    if (!analysisId) return;
    try {
      const res = await apiFetch<any>(`/v1/ai/suggestions/${analysisId}`, { method: 'POST' });
      if (res && res.suggestions) {
        setSuggestions(res.suggestions);
      }
    } catch (e) {
      console.error("Failed to load suggested questions:", e);
    }
  };

  const loadConversationDetails = async (convId: string) => {
    setLoadingHistory(true);
    setErrorMsg(null);
    try {
      const res = await apiFetch<any>(`/v1/ai/conversations/${convId}`);
      if (res && res.messages) {
        setMessages(res.messages);
        setActiveConversationId(convId);
      }
    } catch (e: any) {
      console.error(e);
      setErrorMsg(e.message || "Failed to load chat history.");
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleStartNewChat = () => {
    setActiveConversationId(null);
    setMessages([]);
    setErrorMsg(null);
  };

  const handleDeleteConversation = async (convId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm("Permanently delete this chat history?")) return;
    try {
      await apiFetch<any>(`/v1/ai/conversations/${convId}`, { method: 'DELETE' });
      fetchConversations();
      if (activeConversationId === convId) {
        handleStartNewChat();
      }
    } catch (err: any) {
      alert(err.message || "Failed to delete conversation.");
    }
  };

  const handleSendPrompt = async (text: string) => {
    if (!text.trim() || isGenerating) return;
    
    setInputText('');
    setErrorMsg(null);
    setIsGenerating(true);
    
    // Optimistic User Bubble Append
    const tempUserMsg: Message = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString()
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const response = await apiFetch<any>('/v1/ai/chat', {
        method: 'POST',
        body: JSON.stringify({
          question: text,
          conversation_id: activeConversationId || undefined,
          analysis_id: analysisId || undefined
        })
      });

      if (response && response.answer) {
        const replyMsg: Message = {
          id: Date.now() + 1,
          role: 'model',
          content: response.answer,
          timestamp: new Date().toISOString(),
          key_findings: response.key_findings,
          recommendations: response.recommendations,
          reasoning_summary: response.reasoning_summary,
          citations: response.citations,
          confidence: response.confidence,
          metadata: response.metadata
        };
        
        setMessages((prev) => [...prev, replyMsg]);
        
        if (!activeConversationId) {
          setActiveConversationId(response.conversation_id);
          fetchConversations();
        }
      }
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "Generative analytics pipeline encounterd an error.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-[calc(100vh-6.5rem)] flex gap-4 text-left p-4 overflow-hidden w-full">
      {/* 1. Left Sidebar: Previous Conversations */}
      <div className="w-64 border-r border-slate-200 bg-slate-50 flex flex-col p-4 shrink-0">
        <Button
          onClick={handleStartNewChat}
          className="w-full bg-primary hover:bg-inverse-surface text-on-primary py-2 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all shadow-sm mb-4 cursor-pointer"
        >
          <Plus size={14} />
          New Conversation
        </Button>

        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-2 block">
          Chat History
        </span>

        <div className="flex-1 overflow-y-auto space-y-1 pr-1">
          {conversations.length === 0 ? (
            <div className="text-[11px] text-slate-400 italic text-center py-6">
              No logged chats.
            </div>
          ) : (
            conversations.map((c) => (
              <div
                key={c.conversation_id}
                onClick={() => loadConversationDetails(c.conversation_id)}
                className={`group flex items-center justify-between px-3 py-2.5 rounded-lg text-xs cursor-pointer transition-colors ${
                  activeConversationId === c.conversation_id
                    ? 'bg-blue-50 text-blue-700 font-medium'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <div className="flex items-center gap-2 overflow-hidden flex-1">
                  <MessageSquareCode size={14} className="shrink-0 opacity-80" />
                  <span className="truncate">{c.title}</span>
                </div>
                <button
                  onClick={(e) => handleDeleteConversation(c.conversation_id, e)}
                  className="opacity-0 group-hover:opacity-100 hover:bg-slate-200 p-1 rounded text-slate-400 hover:text-red-600 transition-all ml-1 shrink-0"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* 2. Center Panel: Conversation Dialogue */}
      <div className="flex-1 bg-white border border-slate-200 rounded-xl shadow-sm flex flex-col overflow-hidden">
        {errorMsg && (
          <div className="m-4 p-3.5 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-start gap-2.5 text-xs">
            <AlertCircle className="shrink-0 mt-0.5" size={14} />
            <span className="font-medium">{errorMsg}</span>
          </div>
        )}

        {/* Message Stream */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6">
          {messages.length === 0 && !loadingHistory ? (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 space-y-4">
              <div className="w-14 h-14 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center shadow-inner">
                <Brain size={24} className="text-slate-300" />
              </div>
              <div className="max-w-md space-y-2">
                <h3 className="font-bold text-slate-800 text-lg m-0">InsightPilot Business Analyst</h3>
                <p className="text-xs text-slate-500 max-w-xs mx-auto leading-relaxed">
                  Ask operational queries, request linear summaries, or explore correlation factors. Calculations are computed deterministically.
                </p>
              </div>
            </div>
          ) : loadingHistory ? (
            <div className="h-full flex items-center justify-center text-slate-400">
              <Loader2 className="animate-spin mr-2" size={18} />
              <span className="text-xs font-medium">Loading conversation history...</span>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <div 
                  key={msg.id || i}
                  className={`flex gap-3.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.role !== 'user' && (
                    <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                      <Sparkles size={16} />
                    </div>
                  )}

                  <div className={`max-w-2xl space-y-3.5 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                    {/* Raw Answer Block */}
                    <div className={`p-4 rounded-xl text-xs leading-relaxed shadow-sm ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white font-medium rounded-tr-none'
                        : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none'
                    }`}>
                      {msg.content}
                    </div>

                    {/* AI Structured Additions (Findings, Risks, Confidence, Citations) */}
                    {msg.role !== 'user' && (
                      <div className="space-y-4 pt-1">
                        {/* Findings & Recs */}
                        {((msg.key_findings && msg.key_findings.length > 0) || 
                          (msg.recommendations && msg.recommendations.length > 0)) && (
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                            {msg.key_findings && msg.key_findings.length > 0 && (
                              <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                                <span className="font-bold text-slate-800 uppercase tracking-wider block mb-2">Key Findings</span>
                                <ul className="list-disc pl-4 space-y-1.5 text-slate-600 m-0">
                                  {msg.key_findings.map((kf, idx) => <li key={idx}>{kf}</li>)}
                                </ul>
                              </div>
                            )}
                            {msg.recommendations && msg.recommendations.length > 0 && (
                              <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-3">
                                <span className="font-bold text-blue-800 uppercase tracking-wider block mb-2">Actions Recommended</span>
                                <ul className="list-disc pl-4 space-y-1.5 text-blue-700 m-0">
                                  {msg.recommendations.map((rc, idx) => <li key={idx}>{rc}</li>)}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}

                        {/* Citation Cards */}
                        {msg.citations && msg.citations.length > 0 && (
                          <div>
                            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block mb-2">Factual Citations</span>
                            <div className="flex flex-wrap gap-2">
                              {msg.citations.map((c, idx) => (
                                <div 
                                  key={idx}
                                  title={c.details}
                                  className="group flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[10px] cursor-help transition-all"
                                >
                                  <BookOpen size={10} className="text-slate-400" />
                                  <span className="font-bold text-slate-700">{c.source}</span>
                                  <ExternalLink size={8} className="text-slate-400 opacity-0 group-hover:opacity-100" />
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Confidence score profile */}
                        {msg.confidence && (
                          <div className="flex flex-wrap items-center gap-3 bg-slate-50 border border-slate-200 rounded-lg p-3 text-[10px]">
                            <div className="flex items-center gap-1">
                              <span className="text-slate-400 font-bold uppercase tracking-wider">Factual Confidence:</span>
                              <span className={`font-bold px-2 py-0.5 rounded ${
                                msg.confidence.score >= 80 ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'
                              }`}>
                                {msg.confidence.score}%
                              </span>
                            </div>
                            <div className="flex flex-wrap gap-x-3 gap-y-1 text-slate-500 font-medium">
                              <span>Completeness: {msg.confidence.context_completeness_pct}%</span>
                              <span>Evidence: {msg.confidence.citation_coverage_pct}%</span>
                            </div>
                          </div>
                        )}

                        {/* Observability metadata */}
                        {msg.metadata && (
                          <div className="flex items-center gap-3 text-[9px] text-slate-400 font-bold uppercase tracking-wider">
                            <span className="flex items-center gap-1">
                              <Clock size={10} />
                              {msg.metadata.processing_time}s
                            </span>
                            <span>Cache: {msg.metadata.cache_status}</span>
                            <span>Validation: {msg.metadata.validation_status}</span>
                          </div>
                        )}

                        {/* Fallback warning banner */}
                        {msg.metadata && msg.metadata.fallback_triggered && (
                          <div className="mt-2 text-[10px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-2.5 flex items-center gap-2">
                            <AlertCircle size={14} className="text-amber-600 shrink-0" />
                            <span><strong>Mock Fallback:</strong> The production Gemini service is currently unconfigured or rate-limited. Local mock was utilized.</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Loader with Cycling stages */}
              {isGenerating && (
                <div className="flex gap-3.5 justify-start">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                    <Loader2 className="animate-spin" size={16} />
                  </div>
                  <div className="bg-slate-50 border border-slate-200 p-4 rounded-xl rounded-tl-none text-xs text-slate-500 animate-pulse">
                    {thinkingStages[thinkingIndex]}
                  </div>
                </div>
              )}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Text Box */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex gap-3">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSendPrompt(inputText);
            }}
            placeholder="Ask a question about your data..."
            disabled={isGenerating || !uploadState}
            className="flex-1 bg-white border border-slate-200 rounded-lg px-4 py-2.5 text-xs focus:outline-none focus:border-blue-500 disabled:bg-slate-100 disabled:text-slate-400 caret-black"
          />
          <Button
            onClick={() => handleSendPrompt(inputText)}
            disabled={isGenerating || !inputText.trim() || !uploadState}
            className="px-4 py-2.5 bg-primary hover:bg-inverse-surface text-on-primary font-semibold text-xs rounded-lg flex items-center justify-center gap-1.5 cursor-pointer shadow-sm"
          >
            <Send size={14} />
          </Button>
        </div>
      </div>

      {/* 3. Right Panel: Active Context Summaries */}
      {uploadState && (
        <div className="w-80 bg-slate-50 border border-slate-200 rounded-xl p-5 overflow-y-auto space-y-6 shrink-0 text-xs">
          <div className="border-b border-slate-200 pb-3 flex items-center gap-2">
            <FileSpreadsheet size={16} className="text-blue-600" />
            <h4 className="font-bold text-slate-800 text-sm m-0">Active Context Details</h4>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Domain Type</span>
              <span className="font-semibold text-slate-700 block mt-1 truncate">{uploadState.datasetType || 'Unknown'}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Pulse Rating</span>
              <span className="font-bold text-blue-600 block mt-1">{uploadState.businessPulse ?? 93.3}/100</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Row Size</span>
              <span className="font-semibold text-slate-700 block mt-1">{uploadState.rowsCount?.toLocaleString()}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Quality Score</span>
              <span className="font-semibold text-slate-700 block mt-1">{uploadState.qualityScore}%</span>
            </div>
          </div>

          {/* Top KPIs list */}
          {uploadState.columnMetadata?.columns && (
            <div className="space-y-2">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Key Columns / Features</span>
              <div className="max-h-40 overflow-y-auto space-y-1.5 pr-1">
                {uploadState.columnMetadata.columns.slice(0, 4).map((col: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-2 bg-white border border-slate-200 rounded-lg">
                    <span className="font-medium text-slate-700 truncate max-w-[130px]">{col.name}</span>
                    <span className="text-[9px] px-1.5 py-0.5 bg-blue-50 text-blue-600 font-bold uppercase rounded shrink-0">
                      {col.type}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Dynamic Suggested Questions */}
          {suggestions.length > 0 && (
            <div className="space-y-3 pt-2">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Suggested Questions</span>
              <div className="space-y-2">
                {suggestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendPrompt(q)}
                    disabled={isGenerating}
                    className="w-full text-left p-3 bg-white hover:bg-blue-50/50 border border-slate-200 hover:border-blue-200 rounded-lg text-slate-600 hover:text-blue-700 text-[11px] leading-snug cursor-pointer transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
