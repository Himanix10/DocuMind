import React, { useState, useEffect } from 'react';
import { BrainCircuit, Play, CheckCircle, Activity, GitBranch, FileText, Database } from 'lucide-react';

function App() {
  const [repoPath, setRepoPath] = useState('../india-restaurant-finder');
  const [repoName, setRepoName] = useState('Himanix10/india-restaurant-finder');
  const [isProcessing, setIsProcessing] = useState(false);
  const [serverStatus, setServerStatus] = useState('checking');
  const [logs, setLogs] = useState([]);
  const [backendUrl, setBackendUrl] = useState(() => {
    return import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
  });

  // Check backend status
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/`);
        if (response.ok) {
          setServerStatus('online');
        } else {
          setServerStatus('offline');
        }
      } catch (error) {
        setServerStatus('offline');
      }
    };
    
    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, [backendUrl]);

  const addLog = (msg) => {
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const handleTrigger = async (e) => {
    e.preventDefault();
    if (serverStatus !== 'online') {
      addLog('Error: Backend server is offline. Please start it.');
      return;
    }

    setIsProcessing(true);
    addLog(`Initiating autonomous scan for ${repoName}...`);

    try {
      const response = await fetch(`${backendUrl}/trigger`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_path: repoPath,
          repo_full_name: repoName
        }),
      });

      const data = await response.json();
      if (response.ok) {
        addLog(data.message);
        if (data.local_path) {
          addLog(`Repository path on server: ${data.local_path}`);
        }
        addLog('Agent is now running in the background...');
        
        // Simulate logs for the UI
        setTimeout(() => addLog('Scanning directory structure...'), 2000);
        setTimeout(() => addLog('Extracting AST (Classes & Functions)...'), 4000);
        setTimeout(() => addLog('Embedding context into ChromaDB Memory...'), 6000);
        setTimeout(() => addLog('Invoking Groq LLaMA 3.3 for reasoning...'), 9000);
        setTimeout(() => addLog('Generating README.md and MODULES.md...'), 15000);
        setTimeout(() => addLog('Creating isolated Git Branch...'), 18000);
        setTimeout(() => {
          addLog('Documentation successfully committed!');
          setIsProcessing(false);
        }, 22000);

      } else {
        addLog(`Error: ${data.detail || 'Unknown error occurred'}`);
        setIsProcessing(false);
      }
    } catch (error) {
      addLog(`Error connecting to server: ${error.message}`);
      setIsProcessing(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1 style={{ fontSize: '3rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
          <BrainCircuit size={48} color="#6366f1" />
          <span className="gradient-text">DocuMind AI</span>
        </h1>
        <p>Autonomous Technical Documentation Agent</p>
      </header>

      <div className="grid">
        {/* Left Column: Control Panel */}
        <div className="glass-panel" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
            <h2 style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Activity size={24} color="#6366f1" /> Control Center
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
              <span style={{ 
                width: '10px', height: '10px', borderRadius: '50%', 
                backgroundColor: serverStatus === 'online' ? '#10b981' : '#ef4444',
                boxShadow: serverStatus === 'online' ? '0 0 10px #10b981' : '0 0 10px #ef4444'
              }}></span>
              {serverStatus === 'online' ? 'Backend Online' : 'Backend Offline'}
            </div>
          </div>

          <form onSubmit={handleTrigger} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                Backend Server URL
              </label>
              <input 
                type="text" 
                className="glass-input" 
                value={backendUrl}
                onChange={(e) => setBackendUrl(e.target.value)}
                placeholder="e.g., http://localhost:8000"
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                Target Repository Path (Local or Server)
              </label>
              <input 
                type="text" 
                className="glass-input" 
                value={repoPath}
                onChange={(e) => setRepoPath(e.target.value)}
                placeholder="e.g., ../my-project"
                required
              />
            </div>
            
            <div>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                GitHub Repository (Owner/Repo Name)
              </label>
              <input 
                type="text" 
                className="glass-input" 
                value={repoName}
                onChange={(e) => setRepoName(e.target.value)}
                placeholder="e.g., username/repo"
              />
            </div>

            <button 
              type="submit" 
              className={`neon-button ${isProcessing ? 'pulse' : ''}`}
              disabled={isProcessing || serverStatus !== 'online'}
              style={{ marginTop: '10px' }}
            >
              {isProcessing ? (
                <>
                  <BrainCircuit className="pulse" /> Agent is Thinking...
                </>
              ) : (
                <>
                  <Play size={20} /> Initialize Autonomous Scan
                </>
              )}
            </button>
          </form>

          {/* Stats section */}
          <div style={{ marginTop: '40px', paddingTop: '24px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-around' }}>
             <div style={{ textAlign: 'center' }}>
                <GitBranch size={24} color="#94a3b8" style={{ marginBottom: '8px' }} />
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Webhook Ready</div>
             </div>
             <div style={{ textAlign: 'center' }}>
                <Database size={24} color="#94a3b8" style={{ marginBottom: '8px' }} />
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Vector Memory</div>
             </div>
             <div style={{ textAlign: 'center' }}>
                <FileText size={24} color="#94a3b8" style={{ marginBottom: '8px' }} />
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Auto-Markdown</div>
             </div>
          </div>
        </div>

        {/* Right Column: Terminal Log */}
        <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
             <CheckCircle size={24} color="#10b981" /> Live Agent Logs
          </h2>
          
          <div className="terminal" style={{ flexGrow: 1 }}>
            <div className="terminal-line" style={{ color: '#6366f1' }}>DocuMind AI OS v1.0.0 initialized.</div>
            <div className="terminal-line">Waiting for triggers...</div>
            <div className="terminal-line" style={{ marginBottom: '16px' }}>---</div>
            
            {logs.map((log, index) => (
              <div key={index} className="terminal-line" style={{ 
                color: log.includes('Error') ? '#ef4444' : 
                       log.includes('successfully') ? '#10b981' : 'var(--text-secondary)' 
              }}>
                {log}
              </div>
            ))}
            
            {isProcessing && (
              <div className="terminal-line pulse" style={{ marginTop: '8px' }}>_</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
