import { useState, useEffect } from 'react';
import { ThemeProvider, LanguageProvider } from './contexts';
import { Navigation } from './components/Navigation';
import { HomePage } from './pages/HomePage';
import { DocsPage } from './pages/DocsPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { VideoAnalysisPage } from './pages/VideoAnalysisPage';
import './App.css';

function AppContent() {
  const [currentPage, setCurrentPage] = useState('home');

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '') || 'home';
      setCurrentPage(hash);
    };

    // Set initial page
    handleHashChange();

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navigate = (page: string) => {
    window.location.hash = `/${page === 'home' ? '' : page}`;
  };

  return (
    <div className="app-layout">
      <Navigation currentPage={currentPage} onNavigate={navigate} />

      {currentPage === 'home' ? (
        <HomePage onNavigate={navigate} />
      ) : (
        <div className="page-container">
          {currentPage === 'docs' && <DocsPage />}
          {currentPage === 'analysis' && <AnalysisPage />}
          {currentPage === 'video' && <VideoAnalysisPage />}
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AppContent />
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
