import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface Document {
  id: number;
  filename: string;
  file_type: string;
  created_at: string;
}

interface POC {
  id: number;
  poc_id: string;
  poc_name: string;
  description: string;
  created_at: string;
}

interface Message {
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
}

const POCBuilder: React.FC = () => {
  const { token } = useAuth();
  const [activeTab, setActiveTab] = useState<'documents' | 'pocs'>('documents');
  
  // Documents state
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  
  // POCs state
  const [pocs, setPocs] = useState<POC[]>([]);
  const [selectedPoc, setSelectedPoc] = useState<POC | null>(null);
  
  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadDocuments = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/poc/documents', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  }, [token]);

  const loadPOCs = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/poc/list', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPocs(response.data);
    } catch (error) {
      console.error('Failed to load POCs:', error);
    }
  }, [token]);

  // Load documents and POCs
  useEffect(() => {
    if (token) {
      loadDocuments();
      loadPOCs();
    }
  }, [token, loadDocuments, loadPOCs]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/poc/upload', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      loadDocuments();
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (docId: number) => {
    if (!window.confirm('Delete this document?')) return;

    try {
      await axios.delete(`http://localhost:8000/api/poc/documents/${docId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadDocuments();
    } catch (error) {
      alert('Failed to delete document');
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/poc/chat',
        {
          prompt: input,
          conversation_history: conversationId ? { conversation_id: conversationId } : null
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      const agentMessage: Message = {
        role: 'agent',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, agentMessage]);
      setConversationId(response.data.conversation_id);
    } catch (error: any) {
      const errorMessage: Message = {
        role: 'agent',
        content: 'Error: ' + (error.response?.data?.detail || 'Failed to get response'),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleGeneratePOC = async () => {
    if (!window.confirm('Generate POC with current requirements?')) return;

    setIsTyping(true);
    try {
      const response = await axios.post(
        'http://localhost:8000/api/poc/generate',
        {
          requirements: {} // Will be extracted from conversation
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      const successMessage: Message = {
        role: 'agent',
        content: `POC "${response.data.poc_name}" generated successfully! ID: ${response.data.poc_id}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, successMessage]);
      loadPOCs();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'POC generation failed');
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Panel (40%) */}
      <div className="w-2/5 bg-white border-r flex flex-col">
        {/* Tab Switcher */}
        <div className="flex border-b">
          <button
            className={`flex-1 py-3 px-4 font-medium ${
              activeTab === 'documents'
                ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTab('documents')}
          >
            Documents
          </button>
          <button
            className={`flex-1 py-3 px-4 font-medium ${
              activeTab === 'pocs'
                ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTab('pocs')}
          >
            POCs
          </button>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === 'documents' ? (
            <div>
              {/* Upload Zone */}
              <div className="mb-4">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.txt,.md,.png,.jpg,.jpeg"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className={`block w-full p-6 border-2 border-dashed rounded-lg text-center cursor-pointer transition ${
                    uploading
                      ? 'border-gray-300 bg-gray-50'
                      : 'border-blue-300 hover:border-blue-500 hover:bg-blue-50'
                  }`}
                >
                  {uploading ? (
                    <span className="text-gray-500">Uploading...</span>
                  ) : (
                    <div>
                      <span className="text-blue-600 font-medium">Upload Document</span>
                      <p className="text-sm text-gray-500 mt-1">PDF, TXT, MD, PNG, JPG</p>
                    </div>
                  )}
                </label>
              </div>

              {/* Document List */}
              <div className="space-y-2">
                {documents.length === 0 ? (
                  <p className="text-gray-500 text-sm">No documents uploaded yet</p>
                ) : (
                  documents.map(doc => (
                    <div
                      key={doc.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
                    >
                      <div className="flex-1">
                        <p className="font-medium text-sm">{doc.filename}</p>
                        <p className="text-xs text-gray-500">
                          {doc.file_type.toUpperCase()} • {new Date(doc.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteDocument(doc.id)}
                        className="ml-2 text-red-500 hover:text-red-700"
                      >
                        ×
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {pocs.length === 0 ? (
                <p className="text-gray-500 text-sm">No POCs created yet</p>
              ) : (
                pocs.map(poc => (
                  <div
                    key={poc.id}
                    className={`p-3 rounded-lg cursor-pointer transition ${
                      selectedPoc?.id === poc.id
                        ? 'bg-blue-100 border border-blue-300'
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                    onClick={() => setSelectedPoc(poc)}
                  >
                    <p className="font-medium text-sm">{poc.poc_name}</p>
                    <p className="text-xs text-gray-600 mt-1">{poc.description}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(poc.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>

      {/* Right Panel (60%) */}
      <div className="w-3/5 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b p-4">
          <h1 className="text-xl font-bold text-gray-800">POC Agent</h1>
          <p className="text-sm text-gray-500">Technical Product Manager AI</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm mt-2">Tell me what you'd like to build!</p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                <p className={`text-xs mt-1 ${
                  msg.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-200 rounded-lg p-3">
                <p className="text-sm text-gray-600">Agent is typing...</p>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t p-4">
          <div className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={isTyping || !input.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
          
          {conversationId && (
            <button
              onClick={handleGeneratePOC}
              disabled={isTyping}
              className="mt-2 w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Generate POC
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default POCBuilder;
