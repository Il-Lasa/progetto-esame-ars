import { useState } from 'react';
import axios from 'axios';

function Register({ onRegister }) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [userType, setUserType] = useState('base');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRegister = (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError('Le password non corrispondono.');
      return;
    }

    setError('');

    axios.post('/api/register', {
      email,
      username,
      password,
      user_type: userType
    })
      .then(response => {
        setSuccess('Registrazione avvenuta con successo!');
        onRegister();
      })
      .catch(error => {
        setError('Errore durante la registrazione.');
      });
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Registrati</h2>
        {error && <p className="text-red-500 text-center mb-4">{error}</p>}
        {success && <p className="text-green-500 text-center mb-4">{success}</p>}
        <form onSubmit={handleRegister} className="flex flex-col gap-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="border p-3 rounded-lg"
            required
          />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Nome utente"
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
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Conferma Password"
            className="border p-3 rounded-lg"
            required
          />
          <select
            value={userType}
            onChange={(e) => setUserType(e.target.value)}
            className="border p-3 rounded-lg"
          >
            <option value="base">Base</option>
            <option value="premium">Premium</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit" className="bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition">
            Registrati
          </button>
        </form>
        <div className="mt-4 text-center">
          <p>Hai già un account? <a href="/login" className="text-blue-500">Login</a></p>
        </div>
      </div>
    </div>
  );
}

export default Register;
