import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Link } from 'react-router-dom';
import Home from './Components/Home';
import Register from './Components/Register';
import Login from './Components/Login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const userLoggedIn = localStorage.getItem('isAuthenticated');
    if (userLoggedIn) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
    localStorage.setItem('isAuthenticated', 'true');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
  };

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <nav className="bg-white text-darkGray border-b border-gray-200 p-4">
          <h1 className="text-2xl font-bold">Qualità dell'Aria Puglia</h1>
        </nav>

        <Routes>
          {/* Se l'utente è loggato, mostra la Home, altrimenti reindirizza */}
          <Route path="/" element={isAuthenticated ? <Home /> : <Navigate to="/register" />} />

          {/* Route per la registrazione */}
          <Route path="/register" element={<Register onRegister={handleLogin} />} />

          {/* Route per il login */}
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
        </Routes>

        <footer className="bg-darkGray text-white p-6 text-center">
          <p>© 2024 Qualità dell'Aria Puglia</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
