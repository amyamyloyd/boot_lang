import React from 'react';

interface WelcomeProps {
  userName: string;
  projectName: string;
  githubUrl: string;
}

const Welcome: React.FC<WelcomeProps> = ({ userName, projectName, githubUrl }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white p-8 rounded-lg shadow-2xl">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-6">
          ✅ Boot_Lang Setup Complete!
        </h1>
        
        <div className="space-y-6 text-gray-700">
          <div className="bg-blue-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl">Configuration:</h3>
            <ul className="space-y-2">
              <li><strong>User:</strong> {userName}</li>
              <li><strong>Project:</strong> {projectName}</li>
              <li><strong>GitHub:</strong> <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{githubUrl}</a></li>
            </ul>
          </div>
          
          <div className="bg-green-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-green-800">✓ Environment Ready:</h3>
            <ul className="list-disc list-inside space-y-1">
              <li>Virtual environment created</li>
              <li>Dependencies installed</li>
              <li>Database initialized</li>
              <li>Deployed to Azure</li>
            </ul>
          </div>
          
          <div className="bg-purple-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-purple-800">Tech Stack:</h3>
            <ul className="grid grid-cols-2 gap-2 text-sm">
              <li>• React 18 + TypeScript</li>
              <li>• Tailwind CSS</li>
              <li>• Python 3.11 + FastAPI</li>
              <li>• LangChain + OpenAI</li>
              <li>• SQLite Database</li>
              <li>• Azure App Service</li>
            </ul>
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-yellow-800">Quick Start Commands:</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="bg-white p-2 rounded border"><strong>"Build my PRD"</strong> - Start building from a PRD document</li>
              <li className="bg-white p-2 rounded border"><strong>"Start backend"</strong> - Launch FastAPI server (port 8000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Start frontend"</strong> - Launch React dev server (port 3000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Deploy to Azure"</strong> - Push changes to production</li>
              <li className="bg-white p-2 rounded border"><strong>"Commit the code"</strong> - Stage and commit changes</li>
            </ul>
          </div>
          
          <div className="text-center pt-4">
            <a href="http://localhost:3000" className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold">
              Start Building →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
