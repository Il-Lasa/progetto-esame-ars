import { useState, useEffect } from 'react';
import axios from 'axios';
import MapView from './Components/MapView.jsx';

function App() {
  const [stations, setStations] = useState([]);
  const [selectedStationId, setSelectedStationId] = useState(null);  // Stato per la stazione selezionata

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/stations')
      .then(response => {
        setStations(response.data);
      })
      .catch(error => {
        console.error('Errore durante il caricamento delle stazioni:', error);
      });
  }, []);

  // Funzione per gestire la selezione della stazione
  const handleStationSelect = (event) => {
    setSelectedStationId(event.target.value);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-white text-darkGray border-b border-gray-200 p-4">
        <h1 className="text-2xl font-bold">Qualità dell'Aria Puglia</h1>
      </nav>

      <header className="bg-primary p-10 text-center">
        <h2 className="text-4xl font-bold text-white mb-4">Benvenuto!</h2>
        <p className="text-lg text-white">Monitora la qualità dell'aria nella tua città.</p>
      </header>

      <main className="flex-grow p-10">
        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-darkGray mb-4">Seleziona una stazione</h3>
          <select
            className="bg-white border border-gray-300 rounded-lg p-2 text-darkGray"
            onChange={handleStationSelect}  // Gestore di selezione
          >
            <option value="">-- Seleziona una stazione --</option>
            {stations.map(station => (
              <option key={station.id_station} value={station.id_station}>
                {station.denominazione}
              </option>
            ))}
          </select>
        </section>

        {/* Passa la stazione selezionata alla mappa */}
        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-darkGray mb-4">Mappa delle stazioni</h3>
          <MapView stations={stations} selectedStationId={selectedStationId} />
        </section>
      </main>

      <footer className="bg-darkGray text-white p-6 text-center">
        <p>© 2024 Qualità dell'Aria Puglia</p>
      </footer>
    </div>
  );
}

export default App;