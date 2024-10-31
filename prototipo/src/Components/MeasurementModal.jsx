import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function MeasurementModal({ stationId, onClose }) {
  const [inquinante, setInquinante] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [compareStationId, setCompareStationId] = useState('');
  const [measurements, setMeasurements] = useState([]);
  const [compareMeasurements, setCompareMeasurements] = useState([]);
  const [pollutants, setPollutants] = useState([]);
  const [stations, setStations] = useState([]);

  useEffect(() => {
    const fetchPollutants = async () => {
      try {
        const response = await axios.get('/api/pollutants');
        setPollutants(response.data);
      } catch (error) {
        console.error('Errore nel caricamento degli inquinanti:', error);
      }
    };

    const fetchStations = async () => {
      try {
        const response = await axios.get('/api/stations');
        setStations(response.data);
      } catch (error) {
        console.error('Errore nel caricamento delle stazioni:', error);
      }
    };

    fetchPollutants();
    fetchStations();
  }, []);

  const fetchMeasurements = async () => {
    try {
      const response = await axios.get('/api/station_measurements', {
        params: {
          station_id: stationId,
          inquinante,
          start_date: startDate,
          end_date: endDate,
          compare_station_id: compareStationId
        }
      });
      setMeasurements(response.data.measurements);
      setCompareMeasurements(response.data.compare_measurements);
    } catch (error) {
      console.error('Errore nel caricamento delle misurazioni:', error);
    }
  };

  const chartData = {
    labels: measurements.map(m => m.data),
    datasets: [
      {
        label: `Stazione ${stationId}`,
        data: measurements.map(m => m.valore),
        fill: false,
        borderColor: 'blue',
      },
      compareStationId && {
        label: `Stazione ${compareStationId}`,
        data: compareMeasurements.map(m => m.valore),
        fill: false,
        borderColor: 'red',
      },
    ].filter(Boolean)
  };

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-11/12 h-5/6 flex">
        {/* Area Grafico */}
        <div className="w-3/4 pr-4">
          <Line data={chartData} />
        </div>

        {/* Area Selezioni */}
        <div className="w-1/4 pl-4 flex flex-col space-y-4">
          <h3 className="text-lg font-semibold mb-4">Filtri</h3>

          <select
            value={inquinante}
            onChange={(e) => setInquinante(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="">Seleziona un inquinante</option>
            {pollutants.map((pollutant, index) => (
              <option key={index} value={pollutant}>
                {pollutant}
              </option>
            ))}
          </select>

          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border p-2 rounded"
          />

          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border p-2 rounded"
          />

          <select
            value={compareStationId}
            onChange={(e) => setCompareStationId(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="">Seleziona stazione di confronto (opzionale)</option>
            {stations.map((station) => (
              <option key={station.id_station} value={station.id_station}>
                {station.denominazione}
              </option>
            ))}
          </select>

          <button
            onClick={fetchMeasurements}
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition"
          >
            Visualizza Grafico
          </button>

          <button
            onClick={onClose}
            className="mt-4 bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600 transition"
          >
            Chiudi
          </button>
        </div>
      </div>
    </div>
  );
}

export default MeasurementModal;