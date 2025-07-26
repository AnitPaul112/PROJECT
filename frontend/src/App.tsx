import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface ConversationItem {
  timestamp: string;
  question: string;
  answer: string;
  search_method: string;
}

interface SearchMethod {
  id: string;
  name: string;
  description: string;
}

interface SampleQuestion {
  bangla: string;
  banglish: string;
}

interface ApiResponse {
  answer: string;
  search_method: string;
  relevant_chunks: any[];
  used_conversation_memory: boolean;
  timestamp: string;
  question: string;
  success: boolean;
  error?: string;
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationHistory, setConversationHistory] = useState<ConversationItem[]>([]);
  const [searchMethod, setSearchMethod] = useState('hybrid');
  const [searchMethods, setSearchMethods] = useState<SearchMethod[]>([]);
  const [sampleQuestions, setSampleQuestions] = useState<SampleQuestion[]>([]);
  const [apiStatus, setApiStatus] = useState('checking');
  const [relevantChunks, setRelevantChunks] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<{[key: number]: 'yes' | 'no' | null}>({});
  const [darkMode, setDarkMode] = useState(false);
  const [typedAnswer, setTypedAnswer] = useState('');
  const typingInterval = useRef<NodeJS.Timeout | null>(null);

  // Load search methods and sample questions on component mount
  useEffect(() => {
    loadSearchMethods();
    loadSampleQuestions();
    checkApiStatus();
  }, []);

  // Typing effect for bot answer
  useEffect(() => {
    if (answer && typeof answer === 'string' && answer.length > 0) {
      setTypedAnswer('');
      if (typingInterval.current) clearInterval(typingInterval.current);
      let i = 0;
      typingInterval.current = setInterval(() => {
        setTypedAnswer((prev) => prev + answer[i]);
        i++;
        if (i >= answer.length) {
          if (typingInterval.current) clearInterval(typingInterval.current);
        }
      }, 12); // typing speed
    } else {
      setTypedAnswer('');
      if (typingInterval.current) clearInterval(typingInterval.current);
    }
    // cleanup
    return () => {
      if (typingInterval.current) clearInterval(typingInterval.current);
    };
  }, [answer]);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/`);
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const loadSearchMethods = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/search-methods`);
      setSearchMethods(response.data.methods);
    } catch (error) {
      console.error('Failed to load search methods:', error);
    }
  };

  const loadSampleQuestions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/sample-questions`);
      setSampleQuestions(response.data.questions);
    } catch (error) {
      console.error('Failed to load sample questions:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!question.trim()) {
      setError('প্রশ্ন ফাঁকা রাখা যাবে না!');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post<ApiResponse>(`${API_BASE_URL}/api/query`, {
        question: question.trim(),
        search_method: searchMethod,
        conversation_history: conversationHistory
      });

      const result = response.data;
      
      // Check if API returned an error
      if (!result.success || result.error) {
        setError(result.error || 'একটি অজানা ত্রুটি ঘটেছে');
        setAnswer('');
        return;
      }

      // Ensure answer is valid
      const cleanAnswer = (result.answer || '').toString().trim();
      if (!cleanAnswer) {
        setError('কোনো উত্তর পাওয়া যায়নি। অন্য প্রশ্ন করার চেষ্টা করুন।');
        setAnswer('');
        return;
      }

      setAnswer(cleanAnswer);
      setRelevantChunks(result.relevant_chunks || []);

      // Add to conversation history
      const newConversationItem: ConversationItem = {
        timestamp: new Date().toLocaleTimeString(),
        question: result.question || question.trim(),
        answer: cleanAnswer,
        search_method: result.search_method || searchMethod
      };

      setConversationHistory(prev => [...prev, newConversationItem]);
      setFeedback(prev => ({ ...prev, [conversationHistory.length]: null }));
      setQuestion('');

    } catch (error: any) {
      setAnswer('');
      if (error.response && error.response.data && error.response.data.detail) {
        setError(error.response.data.detail);
      } else {
        setError('দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = (index: number, value: 'yes' | 'no') => {
    setFeedback(prev => ({ ...prev, [index]: value }));
  };

  const handleSampleQuestionClick = (question: string) => {
    setQuestion(question);
  };

  const clearHistory = () => {
    setConversationHistory([]);
    setAnswer('');
    setRelevantChunks([]);
  };

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
  };

  const getSearchMethodName = (methodId: string) => {
    const method = searchMethods.find(m => m.id === methodId);
    return method ? method.name : methodId;
  };

  // Copy Answer
  const handleCopyAnswer = () => {
    if (answer) {
      navigator.clipboard.writeText(answer);
    }
  };

  // Text-to-Speech (Read Aloud)
  const handleReadAloud = () => {
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support Text-to-Speech.');
      return;
    }
    const utter = new window.SpeechSynthesisUtterance(answer);
    utter.lang = 'bn-BD';
    window.speechSynthesis.cancel(); // stop previous
    window.speechSynthesis.speak(utter);
  };

  return (
    <div className={`App${darkMode ? ' dark' : ''}`}>
      {/* Loading Spinner Overlay */}
      {loading && (
        <div className="spinner-overlay">
          <div className="spinner"></div>
        </div>
      )}
      <div className="container">
        {/* Header */}
        <header className="header">
          <h1 className="title">অপরিচিতা</h1>
          <p className="subtitle">আলোচ্য বিষয় 'অপরিচিতা' গল্প</p>
          <div className={`status-indicator ${apiStatus}`}>
            {apiStatus === 'connected' ? '🟢 API সংযুক্ত' : 
             apiStatus === 'disconnected' ? '🔴 API সংযোগ নেই' : '🟡 পরীক্ষা করছে...'}
          </div>
          <button className="darkmode-toggle" onClick={toggleDarkMode}>
            {darkMode ? '🌙 ডার্ক' : '☀️ লাইট'}
          </button>
        </header>

        <div className="main-content">
          {/* Left Panel - Chat Interface */}
          <div className="chat-panel">
            {/* Error Message */}
            {error && (
              <div className="error-message">
                <span>⚠️</span> {error}
              </div>
            )}
            {/* Question Input */}
            <form onSubmit={handleSubmit} className="question-form">
              <div className="input-group">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="আপনার প্রশ্ন লিখুন... (যেমন: anupamer boyosh koto?)"
                  className="question-input"
                  disabled={loading}
                />
                <button type="submit" className="submit-btn" disabled={loading || !question.trim()}>
                  {loading ? '🔍 খুঁজছে...' : 'জিজ্ঞাসা করুন'}
                </button>
              </div>

              {/* Search Method Selection */}
              <div className="search-method-selector">
                <label>সার্চ পদ্ধতি:</label>
                <select 
                  value={searchMethod} 
                  onChange={(e) => setSearchMethod(e.target.value)}
                  className="method-select"
                >
                  {searchMethods.map(method => (
                    <option key={method.id} value={method.id}>
                      {method.name}
                    </option>
                  ))}
                </select>
              </div>
            </form>

            {/* Answer Display */}
            {answer && (
              <div className="answer-section">
                <h3>উত্তর:</h3>
                <div className="answer-content">
                  <span className="typing-effect">{typedAnswer}</span>
                  <button className="copy-btn" onClick={handleCopyAnswer} title="Copy Answer">📋</button>
                  <button className="tts-btn" onClick={handleReadAloud} title="Read Aloud">🔊</button>
                </div>
                {relevantChunks.length > 0 && (
                  <div className="relevant-chunks">
                    <h4>প্রাসঙ্গিক তথ্যসূত্র:</h4>
                    {relevantChunks.slice(0, 3).map((chunk, index) => (
                      <div key={index} className="chunk-item">
                        <p>{chunk.text.substring(0, 200)}...</p>
                      </div>
                    ))}
                  </div>
                )}
                {/* User Feedback */}
                <div className="feedback-section">
                  <span>এই উত্তরটি কি আপনার জন্য সহায়ক ছিল?</span>
                  <button
                    className={`feedback-btn yes${feedback[conversationHistory.length-1] === 'yes' ? ' selected' : ''}`}
                    onClick={() => handleFeedback(conversationHistory.length-1, 'yes')}
                    disabled={feedback[conversationHistory.length-1] !== null}
                  >হ্যাঁ</button>
                  <button
                    className={`feedback-btn no${feedback[conversationHistory.length-1] === 'no' ? ' selected' : ''}`}
                    onClick={() => handleFeedback(conversationHistory.length-1, 'no')}
                    disabled={feedback[conversationHistory.length-1] !== null}
                  >না</button>
                  {feedback[conversationHistory.length-1] && (
                    <span className="feedback-thankyou">ধন্যবাদ!</span>
                  )}
                </div>
              </div>
            )}

            {/* Sample Questions */}
            <div className="sample-questions">
              <h3>নমুনা প্রশ্ন:</h3>
              <div className="question-grid">
                {sampleQuestions.map((q, index) => (
                  <button
                    key={index}
                    onClick={() => handleSampleQuestionClick(q.bangla)}
                    className="sample-question-btn"
                  >
                    <div className="bangla-text">{q.bangla}</div>
                    <div className="banglish-text">{q.banglish}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right Panel - Conversation History */}
          <div className="history-panel">
            <div className="history-header">
              <h3>কথোপকথনের ইতিহাস</h3>
              <button onClick={clearHistory} className="clear-btn">
                🗑️ মুছুন
              </button>
            </div>
            
            <div className="conversation-list">
              {conversationHistory.length === 0 ? (
                <p className="no-history">কোন কথোপকথন নেই</p>
              ) : (
                conversationHistory.slice(-5).reverse().map((item, index) => (
                  <div key={index} className="conversation-item">
                    <div className="conversation-header">
                      <span className="timestamp">🕐 {item.timestamp}</span>
                      <span className="method-badge">{getSearchMethodName(item.search_method)}</span>
                    </div>
                    <div className="question-text">❓ {item.question}</div>
                    <div className="answer-text">💬 {item.answer.substring(0, 100)}...</div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
