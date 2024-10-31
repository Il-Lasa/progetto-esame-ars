import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useState, useEffect } from 'react';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

function MapView({ stations, selectedStationId }) {
  // Icona di default per i marker selezionati (dimensioni normali)
  const defaultIcon = new L.Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    iconSize: [25, 41],  // Dimensioni standard del marker
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // Icona ridotta per i marker non selezionati (50% più piccoli)
  const smallIcon = new L.Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    iconSize: [12.5, 20.5],  // Dimensioni ridotte del 50%
    iconAnchor: [6.25, 20.5],
    popupAnchor: [0.5, -17],
    shadowSize: [20.5, 20.5]
  });

  return (
    <MapContainer center={[40.66, 17.94]} zoom={8} scrollWheelZoom={false} style={{ height: '400px', width: '100%', zIndex: 0 }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {stations.map(station => {
        if (!station.coordinates) {
          console.error(`Stazione ${station.id_station} non ha coordinate valide.`);
          return null;
        }

        const coordinates = station.coordinates
          .replace('[', '')
          .replace(']', '')
          .split(',')
          .map(coord => parseFloat(coord.trim()));

        const latLng = [coordinates[1], coordinates[0]];

        if (isNaN(latLng[0]) || isNaN(latLng[1])) {
          console.error(`Coordinate non valide per la stazione ${station.id_station}: ${station.coordinates}`);
          return null;
        }

        const isSelected = station.id_station === selectedStationId;

        const markerIcon = isSelected || !selectedStationId ? defaultIcon : smallIcon;

        return (
          <Marker key={station.id_station} position={latLng} icon={markerIcon}>
            <Popup>
              <strong>{station.denominazione}</strong><br />
              {station.comune}, {station.provincia}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}

export default MapView;