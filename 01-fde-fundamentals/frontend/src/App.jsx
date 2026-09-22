import React, { useState, useEffect } from 'react';
import {
  Bot,
  Cpu,
  GitMerge,
  Sparkles,
  Send,
  Database,
  FileText,
  History,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  Search,
  Layers,
  ArrowRight
} from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const PRESET_QUERIES = [
  { label: '📦 Order Status', query: 'Where is my order status for ORD-1003?' },
  { label: '✅ Damaged Item (Eligible - 3 Days)', query: 'I received a broken item for ORD-1001 3 days ago. Can I replace it?' },
  { label: '❌ Exchange Request (Expired - 12 Days)', query: 'I want to exchange my gaming laptop for ORD-1002 delivered 12 days ago.' },
  { label: '🌐 Hinglish Query (Fails Rule-Based)', query: "My parcel hasn't arrived yet! Delivery kab hogi?" },
  { label: '💳 Refund Query', query: 'Can I get my money back for my order?' }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('explorer'); // 'explorer', 'comparison', 'inspector', 'history'
  const [queryInput, setQueryInput] = useState('I received a broken item for ORD-1001 3 days ago. Can I replace it?');
  const [selectedStage, setSelectedStage] = useState('all'); // 'all', 'stage1', 'stage2', 'stage3', 'stage4'
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [expandedTrace, setExpandedTrace] = useState({ stage1: true, stage2: true, stage3: true, stage4: true });
  const [history, setHistory] = useState([]);
  const [erpOrders, setErpOrders] = useState({});
  const [policies, setPolicies] = useState([]);
  const [apiConnected, setApiConnected] = useState(true);

  // Fetch ERP Orders & Policies on mount
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [ordersRes, policiesRes] = await Promise.all([
        fetch(`${API_BASE_URL}/erp-orders`),
        fetch(`${API_BASE_URL}/policies`)
      ]);
      if (ordersRes.ok && policiesRes.ok) {
        setErpOrders(await ordersRes.json());
        setPolicies(await policiesRes.json());
        setApiConnected(true);
      }
    } catch (err) {
      console.error("Failed to connect to backend API:", err);
      setApiConnected(false);
    }
  };

  const handleQuerySubmit = async (e) => {
    if (e) e.preventDefault();
    if (!queryInput.trim() || loading) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryInput,
          stage: selectedStage
        })
      });

      if (!res.ok) throw new Error('API Error');

      const data = await res.json();
      setResults(data);
      setApiConnected(true);

      // Add to History
      setHistory(prev => [{
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        query: queryInput,
        data: data
      }, ...prev]);

    } catch (err) {
      console.error(err);
      alert('Could not process query. Please ensure backend server is running at http://127.0.0.1:8000');
      setApiConnected(false);
    } finally {
      setLoading(false);
    }
  };

  const toggleTrace = (stageKey) => {
    setExpandedTrace(prev => ({ ...prev, [stageKey]: !prev[stageKey] }));
  };

  const getStageIcon = (stageId) => {
    switch (stageId) {
      case 'stage1': return <Bot className="w-5 h-5 text-red-400" />;
      case 'stage2': return <Cpu className="w-5 h-5 text-yellow-400" />;
      case 'stage3': return <GitMerge className="w-5 h-5 text-blue-400" />;
      case 'stage4': return <Sparkles className="w-5 h-5 text-purple-400" />;
      default: return <Layers className="w-5 h-5 text-sky-400" />;
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header glass-panel">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <div className="brand-title gradient-text">FDE Support AI Engine</div>
            <div className="brand-subtitle">Forward Deployed Engineering • 4-Stage Enterprise Support Evolution</div>
          </div>
        </div>
        <div className="status-badge">
          <span className="status-dot"></span>
          {apiConnected ? 'API Connected (Port 8000)' : 'API Offline'}
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="nav-tabs">
        <button
          className={`tab-btn ${activeTab === 'explorer' ? 'active' : ''}`}
          onClick={() => setActiveTab('explorer')}
        >
          <Layers className="w-4 h-4" /> AI Query & Stage Explorer
        </button>
        <button
          className={`tab-btn ${activeTab === 'comparison' ? 'active' : ''}`}
          onClick={() => setActiveTab('comparison')}
        >
          <GitMerge className="w-4 h-4" /> 4-Stage Comparison Matrix
        </button>
        <button
          className={`tab-btn ${activeTab === 'inspector' ? 'active' : ''}`}
          onClick={() => setActiveTab('inspector')}
        >
          <Database className="w-4 h-4" /> ERP Database & Policy Inspector
        </button>
        <button
          className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <History className="w-4 h-4" /> Ticket Query History ({history.length})
        </button>
      </div>

      {/* Main Tab Content */}
      {activeTab === 'explorer' || activeTab === 'comparison' ? (
        <>
          {/* Query Ingestion Section */}
          <div className="query-section glass-panel">
            <div className="section-label">Select Sample Preset Query</div>
            <div className="preset-chips">
              {PRESET_QUERIES.map((preset, idx) => (
                <button
                  key={idx}
                  className="chip"
                  onClick={() => setQueryInput(preset.query)}
                >
                  {preset.label}
                </button>
              ))}
            </div>

            <form onSubmit={handleQuerySubmit} className="input-container">
              <textarea
                className="query-textarea"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                placeholder="Enter customer support ticket query (e.g. 'Where is my order status for ORD-1001?')..."
                rows={3}
              />
              <div className="input-controls">
                <div className="stage-selector">
                  <span className="selector-label">Target Engine:</span>
                  <select
                    className="custom-select"
                    value={selectedStage}
                    onChange={(e) => setSelectedStage(e.target.value)}
                  >
                    <option value="all">⚡ All 4 Stages (Comparative Analysis)</option>
                    <option value="stage1">Stage 1: Hardcoded Rule-Based System</option>
                    <option value="stage2">Stage 2: ML Intent Classifier</option>
                    <option value="stage3">Stage 3: Hybrid Engine (ML + ERP DB + Policy Matrix)</option>
                    <option value="stage4">Stage 4: Generative AI Agent + Policy RAG + ERP Tools</option>
                  </select>
                </div>

                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" /> Processing AI Engines...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4" /> Submit Query to System
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Results Output Section */}
          {results && results.results && (
            <div className="stages-grid">
              {Object.entries(results.results).map(([stageKey, stageData]) => (
                <div key={stageKey} className={`stage-card glass-panel ${stageKey}`}>
                  <div className="card-header">
                    <div>
                      <div className="stage-tag">{stageData.stage_id.toUpperCase()}</div>
                      <div className="card-title">{stageData.stage_name}</div>
                    </div>
                    <div className={`status-indicator ${stageData.status}`}>
                      {stageData.status}
                    </div>
                  </div>

                  {/* Metadata Bar */}
                  <div className="meta-grid">
                    <div className="meta-item">
                      <span className="meta-label">Detected Intent</span>
                      <span className="meta-value">{stageData.intent || 'N/A'}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-label">Confidence Score</span>
                      <span className="meta-value">
                        {stageData.confidence !== null ? `${(stageData.confidence * 100).toFixed(1)}%` : 'N/A'}
                      </span>
                      {stageData.confidence !== null && (
                        <div className="confidence-bar">
                          <div
                            className="confidence-fill"
                            style={{ width: `${Math.min(100, stageData.confidence * 100)}%` }}
                          />
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Final Response Output */}
                  <div className="response-box">
                    {stageData.response}
                  </div>

                  {/* Step-by-Step Execution Trace Log Accordion */}
                  {stageData.logs && stageData.logs.length > 0 && (
                    <div className="trace-accordion">
                      <div
                        className="trace-header"
                        onClick={() => toggleTrace(stageKey)}
                      >
                        <span>Step-by-Step Execution Trace ({stageData.logs.length} Steps)</span>
                        {expandedTrace[stageKey] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </div>
                      {expandedTrace[stageKey] && (
                        <div className="trace-content">
                          {stageData.logs.map((log, lIdx) => (
                            <div
                              key={lIdx}
                              className={`log-item ${log.includes('SUCCESS') || log.includes('APPROVED') || log.includes('Context Injected') ? 'highlight' : ''}`}
                            >
                              {log}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </>
      ) : null}

      {/* Inspector Tab Content */}
      {activeTab === 'inspector' && (
        <div className="inspector-grid">
          {/* ERP Order Records */}
          <div className="inspect-card glass-panel">
            <div className="brand" style={{ marginBottom: '16px' }}>
              <Database className="w-5 h-5 text-sky-400" />
              <h3>Enterprise ERP Order Database Records</h3>
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Mock ERP Database table queried by Stage 3 (Hybrid Engine) & Stage 4 (GenAI Agent).
            </p>

            <table className="order-table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer</th>
                  <th>Product</th>
                  <th>Delivery Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.values(erpOrders).map((order) => (
                  <tr key={order.order_id}>
                    <td><strong style={{ color: 'var(--primary)' }}>{order.order_id}</strong></td>
                    <td>{order.customer_name}</td>
                    <td>{order.product}</td>
                    <td>{order.delivery_date || 'N/A'}</td>
                    <td>
                      <span className={`status-indicator ${order.status === 'DELIVERED' ? 'SUCCESS' : 'CLASSIFIED'}`}>
                        {order.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* RAG Policy Base */}
          <div className="inspect-card glass-panel">
            <div className="brand" style={{ marginBottom: '16px' }}>
              <FileText className="w-5 h-5 text-purple-400" />
              <h3>Enterprise Knowledge Base Policies (RAG)</h3>
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Policy documents indexed by PolicyRAGEngine for semantic vector retrieval.
            </p>

            <div className="policy-list">
              {policies.map((pol) => (
                <div key={pol.id} className="policy-card">
                  <div className="policy-title">[{pol.id}] {pol.title}</div>
                  <div className="policy-desc">{pol.content}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* History Tab Content */}
      {activeTab === 'history' && (
        <div className="history-list">
          {history.length === 0 ? (
            <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
              No ticket query history yet. Submit queries in the Explorer tab!
            </div>
          ) : (
            history.map((item) => (
              <div key={item.id} className="history-item glass-panel">
                <div className="history-header">
                  <span>Timestamp: {item.timestamp}</span>
                  <span>Extracted Order ID: {item.data.extracted_order_id || 'None'}</span>
                </div>
                <div className="history-query">"{item.query}"</div>

                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  {Object.entries(item.data.results || {}).map(([sKey, sRes]) => (
                    <div key={sKey} className={`status-indicator ${sRes.status}`}>
                      {sKey.toUpperCase()}: {sRes.intent} ({sRes.status})
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
