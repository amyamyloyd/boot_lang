import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config';

const POCBuilder: React.FC = () => {
  const [description, setDescription] = useState('');
  const [pocResult, setPocResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/poc/create`, {
        description,
        user_id: 'demo_user'
      });
      setPocResult(response.data);
    } catch (error) {
      console.error('Failed to create POC:', error);
    }
    setLoading(false);
  };

  return (
    <div className="flex h-screen">
      {/* Left Panel 40% */}
      <div className="w-2/5 bg-gray-100 p-6 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-4">POC Builder</h2>
        
        <textarea
          className="w-full h-64 p-4 border rounded mb-4"
          placeholder="Describe what you want to build..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        
        <button
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate POC'}
        </button>
      </div>

      {/* Right Panel 60% */}
      <div className="w-3/5 bg-white p-6 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-4">POC Output</h2>
        
        {pocResult ? (
          <div>
            <div className="mb-4">
              <strong>POC ID:</strong> {pocResult.poc_id}
            </div>
            <div className="mb-4">
              <strong>Structure:</strong>
              <pre className="bg-gray-100 p-4 rounded mt-2">
                {JSON.stringify(pocResult.poc_structure, null, 2)}
              </pre>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">Submit a description to generate a POC...</p>
        )}
      </div>
    </div>
  );
};

export default POCBuilder;