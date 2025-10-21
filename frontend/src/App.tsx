import React from 'react';
import Welcome from './components/Welcome';

const App: React.FC = () => {
  // Load config from window object (injected during build)
  const config = (window as any).bootLangConfig || {
    userName: 'User',
    projectName: 'Boot_Lang Project',
    githubUrl: 'https://github.com'
  };

  return <Welcome {...config} />;
};

export default App;
