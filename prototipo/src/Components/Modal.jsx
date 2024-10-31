import React from 'react';

function Modal({ message, onClose, showTable, measurements }) {
  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-1/2">
        <p className="text-lg mb-4">{message}</p>

        {showTable && (
          <div className="overflow-y-auto max-h-80 mb-4">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="border px-4 py-2">Inquinante</th>
                  <th className="border px-4 py-2">Valore</th>
                  <th className="border px-4 py-2">Stazione</th>
                  <th className="border px-4 py-2">Superamenti</th>
                  <th className="border px-4 py-2">Indice Qualità</th>
                  <th className="border px-4 py-2">Denominazione</th>
                </tr>
              </thead>
              <tbody>
                {measurements.map((measurement, index) => (
                  <tr key={index}>
                    <td className="border px-4 py-2">{measurement.inquinante_misurato}</td>
                    <td className="border px-4 py-2">{measurement.valore_inquinante_misurato}</td>
                    <td className="border px-4 py-2">{measurement.id_station}</td>
                    <td className="border px-4 py-2">{measurement.superamenti}</td>
                    <td className="border px-4 py-2">{measurement.indice_qualita}</td>
                    <td className="border px-4 py-2">{measurement.denominazione}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <button
          onClick={onClose}
          className="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition"
        >
          Chiudi
        </button>
      </div>
    </div>
  );
}

export default Modal;