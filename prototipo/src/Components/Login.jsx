import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');

    axios.post('http://localhost:5000/api/login', {
      email,
      password
    })
      .then(response => {
        const { access_token } = response.data;

        localStorage.setItem('access_token', access_token);

        onLogin();
        navigate('/');
      })
      .catch(error => {
        setError('Email o password errati.');
      });
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        {error && <p className="text-red-500 text-center mb-4">{error}</p>}
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="border p-3 rounded-lg"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="border p-3 rounded-lg"
            required
          />
          <button type="submit" className="bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition">
            Login
          </button>
        </form>
        <div className="mt-4 text-center">
          <p>Non hai un account? <a href="/register" className="text-blue-500">Registrati</a></p>
        </div>
      </div>
    </div>
  );
}

export default Login;
