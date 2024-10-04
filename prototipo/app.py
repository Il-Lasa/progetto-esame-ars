from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa flask-cors
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte

# Configurazione del database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "arpa.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definizione del modello per le tabelle nel database
class Station(db.Model):
    __tablename__ = 'stations'
    id_station = db.Column(db.String, primary_key=True)
    denominazione = db.Column(db.String)
    coordinates = db.Column(db.String)
    rete = db.Column(db.String)
    interesse_rete = db.Column(db.String)
    tipologia_stazione = db.Column(db.String)
    tipologia_area = db.Column(db.String)
    comune = db.Column(db.String)
    provincia = db.Column(db.String)
    paese = db.Column(db.String)
    paese_esteso = db.Column(db.String)

class Measurement(db.Model):
    __tablename__ = 'measurements'
    data_rilevazione = db.Column(db.String, primary_key=True)
    inquinante_misurato = db.Column(db.String)
    id_station = db.Column(db.String, db.ForeignKey('stations.id_station'))
    valore_inquinante_misurato = db.Column(db.Float)
    superamenti = db.Column(db.Integer)
    indice_qualita = db.Column(db.Float)
    responsabile_dato = db.Column(db.String)
    punto_di_contatto = db.Column(db.String)
    sorgente = db.Column(db.String)
    marker_color = db.Column(db.String)

# Rotta per ottenere tutte le stazioni
@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([{
        'id_station': station.id_station,
        'denominazione': station.denominazione,
        'coordinates': station.coordinates,
        'rete': station.rete,
        'comune': station.comune,
        'provincia': station.provincia
    } for station in stations])

# Rotta per ottenere tutte le misurazioni
@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    measurements = Measurement.query.all()
    return jsonify([{
        'data_rilevazione': measurement.data_rilevazione,
        'inquinante_misurato': measurement.inquinante_misurato,
        'id_station': measurement.id_station,
        'valore_inquinante_misurato': measurement.valore_inquinante_misurato,
        'indice_qualita': measurement.indice_qualita,
        'marker_color': measurement.marker_color
    } for measurement in measurements])

if __name__ == '__main__':
    app.run(debug=True)