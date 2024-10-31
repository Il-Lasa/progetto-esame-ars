import { useState, useEffect } from 'react';
import axios from 'axios';

function Profile({ onLogout }) {
  const [userData, setUserData] = useState({ username: '', email: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    axios.get('/api/profile', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        setUserData(response.data);
      })
      .catch(err => {
        setError("Errore nel recuperare i dati del profilo");
        console.error(err);
      });
  }, []);

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md text-center">
        <h2 className="text-2xl font-bold mb-6">Profilo Utente</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <p className="text-lg"><strong>Nome utente:</strong> {userData.username}</p>
        <p className="text-lg mb-4"><strong>Email:</strong> {userData.email}</p>
        <button onClick={onLogout} className="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600">
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;