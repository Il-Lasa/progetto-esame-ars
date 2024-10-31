import { useState, useEffect } from 'react';
import axios from 'axios';
import MapView from './MapView';
import { Link } from 'react-router-dom';
import Modal from './Modal';

function Home() {
  const [stations, setStations] = useState([]);
  const [selectedStationId, setSelectedStationId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [measurements, setMeasurements] = useState([]);
  const [showTable, setShowTable] = useState(false);

  const handleDownloadData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('/api/update_data');
      setModalMessage(response.data.message);
      setIsModalOpen(true);
    } catch (error) {
      setModalMessage('Errore durante il download dei dati');
      setIsModalOpen(true);
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const showLatestMeasurements = async () => {
    try {
      const response = await axios.get('/api/latest_measurements');
      setMeasurements(response.data.measurements);
      setModalMessage(`Dati più recenti (${response.data.date})`);
      setShowTable(true);
      setIsModalOpen(true);
    } catch (error) {
      setModalMessage('Nessun dato disponibile');
      setIsModalOpen(true);
      console.error("Errore nel caricamento dei dati più recenti:", error);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setShowTable(false);
  };

  useEffect(() => {
    axios.get('/api/stations')
      .then(response => setStations(response.data))
      .catch(error => console.error('Errore durante il caricamento delle stazioni:', error));
  }, []);

  const handleStationSelect = (event) => setSelectedStationId(event.target.value);

  return (
    <>
      <header className="bg-primary p-10 text-center">
        <h2 className="text-4xl font-bold text-white mb-4">Benvenuto!</h2>
        <p className="text-lg text-white mb-6">Monitora la qualità dell'aria nella tua città.</p>
        <Link to="/profile" className="bg-blue-500 text-white py-2 px-4 mt-4 rounded-lg hover:bg-blue-600 transition">
          Vai al Profilo
        </Link>
      </header>

      <main className="flex-grow p-10">
        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-darkGray mb-4">Seleziona una stazione</h3>
          <div className="flex justify-between items-center">
            <div className="w-1/3">
              <select
                className="bg-white border border-gray-300 rounded-lg p-2 text-darkGray w-full"
                onChange={handleStationSelect}
              >
                <option value="">-- Seleziona una stazione --</option>
                {stations.map(station => (
                  <option key={station.id_station} value={station.id_station}>
                    {station.denominazione}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleDownloadData}
                className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition"
                disabled={isLoading}
              >
                {isLoading ? 'Caricamento...' : 'Scarica dati'}
              </button>
              <button
                onClick={showLatestMeasurements}
                className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition"
              >
                Mostra i dati più recenti
              </button>
            </div>
          </div>
        </section>

        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-darkGray mb-4">Mappa delle stazioni</h3>
          <MapView stations={stations} selectedStationId={selectedStationId} />
        </section>

        {isModalOpen && (
          <Modal
            message={modalMessage}
            onClose={closeModal}
            showTable={showTable}
            measurements={measurements}
          />
        )}
      </main>
    </>
  );
}

export default Home;