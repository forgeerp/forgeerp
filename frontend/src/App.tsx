import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { isAuthenticated } from './lib/auth';
import { Login } from './components/Login';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Clients } from './components/Clients';
import { Configurations } from './pages/Configurations';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
    setChecking(false);
  }, []);

  const handleLogin = () => {
    setAuthenticated(true);
  };

  if (checking) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-gray-600">Verificando autenticação...</div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={
          !authenticated ? (
            <Login onLogin={handleLogin} />
          ) : (
            <Navigate to="/" replace />
          )
        } />
        <Route path="/" element={
          authenticated ? (
            <Layout>
              <Dashboard />
            </Layout>
          ) : (
            <Navigate to="/login" replace />
          )
        } />
        <Route path="/clients" element={
          authenticated ? (
            <Layout>
              <Clients />
            </Layout>
          ) : (
            <Navigate to="/login" replace />
          )
        } />
        <Route path="/configurations" element={
          authenticated ? (
            <Layout>
              <Configurations />
            </Layout>
          ) : (
            <Navigate to="/login" replace />
          )
        } />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
