from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import os
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests
import pandas as pd  
import sqlite3  
from datetime import date

app = Flask(__name__)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app.config['SQLALCHEMY_BINDS'] = {
    'arpa': f'sqlite:///{os.path.join(basedir, "arpa.db")}',
    'users': f'sqlite:///{os.path.join(basedir, "prototipo", "users.db")}'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Station(db.Model):
    __bind_key__ = 'arpa'
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
    __bind_key__ = 'arpa'
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

class User(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='base')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Il proxy di Vite funziona!"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', 'base')

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "Utente già registrato"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, username=username, password_hash=password_hash, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email)

    return jsonify({"message": "Registrazione avvenuta con successo", "access_token": access_token}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Email o password errati"}), 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Email o password errati"}), 401

    access_token = create_access_token(identity=email)

    return jsonify({"message": "Login avvenuto con successo", "access_token": access_token}), 200

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

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    user_email = get_jwt_identity()
    
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "Utente non trovato"}), 404
    
    return jsonify({
        "email": user.email,
        "username": user.username
    }), 200

@app.route('/api/update_data', methods=['POST'])
def update_data():
    url = "http://old.arpa.puglia.it/ARPA_ARIA/dati.jsp?format=GeoJSON"
    print(f"Prendendo i dati da {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return jsonify({"error": "Nessun dato ricevuto"}), 500
        
        print("Dati recuperati con successo")
        
        features = data['features']
        df = pd.json_normalize(features)
        
        conn = sqlite3.connect('arpa.db')
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
            INSERT OR IGNORE INTO stations (
                id_station, denominazione, coordinates, rete, interesse_rete,
                tipologia_stazione, tipologia_area, comune, provincia, paese, paese_esteso
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['properties.id_station'], row['properties.denominazione'], 
                str(row['geometry.coordinates']), row['properties.rete'], 
                row['properties.interesse_rete'], row['properties.tipologia_di_stazione'], 
                row['properties.tipologia_di_area'], row['properties.comune'], 
                row['properties.provincia'], row['properties.paese'], 
                row['properties.paese_esteso']
            ))

        for _, row in df.iterrows():
            cursor.execute('''
            INSERT OR IGNORE INTO pollutants (
                inquinante_misurato, limite, unita_misura
            ) VALUES (?, ?, ?)
            ''', (
                row['properties.inquinante_misurato'], row['properties.limite'], row['properties.unita_misura']
            ))

        conn.commit()

        new_data_added = False

        for _, row in df.iterrows():
            cursor.execute('''
            SELECT COUNT(*)
            FROM measurements
            WHERE data_rilevazione = ? AND inquinante_misurato = ? AND id_station = ?
            ''', (row['properties.data_di_misurazione'], row['properties.inquinante_misurato'], row['properties.id_station']))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                new_data_added = True
                cursor.execute('''
                INSERT INTO measurements (
                    data_rilevazione, inquinante_misurato, id_station, 
                    valore_inquinante_misurato, superamenti, indice_qualita, 
                    responsabile_dato, punto_di_contatto, sorgente, marker_color
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['properties.data_di_misurazione'], row['properties.inquinante_misurato'], 
                    row['properties.id_station'], row['properties.valore_inquinante_misurato'], 
                    row['properties.superamenti'], row['properties.indice_qualita'], 
                    row['properties.responsabile_dato'], row['properties.punto_di_contatto'], 
                    row['properties.sorgente'], row['properties.marker-color']
                ))

        conn.commit()
        conn.close()

        if new_data_added:
            return jsonify({"message": "Dati scaricati e aggiornati con successo"}), 200
        else:
            return jsonify({"message": "I dati sono già aggiornati"}), 200
    
    except requests.exceptions.RequestException as e:
        print("Errore durante la richiesta HTTP:", e)
        return jsonify({"error": "Errore durante la richiesta HTTP"}), 500
    except sqlite3.Error as e:
        print("Errore durante l'inserimento nel database:", e)
        return jsonify({"error": "Errore durante l'inserimento nel database"}), 500
    except Exception as e:
        print("Errore generico:", e)
        return jsonify({"error": "Errore generico"}), 500
    
@app.route('/api/latest_measurements', methods=['GET'])
def latest_measurements():
    conn = sqlite3.connect('arpa.db')
    cursor = conn.cursor()

    today = date.today().strftime('%Y-%m-%d')

    cursor.execute('''
        SELECT data_rilevazione
        FROM measurements
        WHERE data_rilevazione <= ?
        ORDER BY ABS(JULIANDAY(data_rilevazione) - JULIANDAY(?)) ASC
        LIMIT 1
    ''', (today, today))
    
    result = cursor.fetchone()

    if result:
        selected_date = result[0]
        
        cursor.execute('''
            SELECT m.data_rilevazione, m.inquinante_misurato, m.id_station, 
                   m.valore_inquinante_misurato, m.superamenti, m.indice_qualita, s.denominazione
            FROM measurements m
            JOIN stations s ON m.id_station = s.id_station
            WHERE m.data_rilevazione = ?
        ''', (selected_date,))
        
        measurements = [{
            "data_rilevazione": row[0],
            "inquinante_misurato": row[1],
            "id_station": row[2],
            "valore_inquinante_misurato": row[3],
            "superamenti": row[4],
            "indice_qualita": row[5],
            "denominazione": row[6]
        } for row in cursor.fetchall()]

        conn.close()
        return jsonify({"measurements": measurements, "date": selected_date}), 200
    else:
        conn.close()
        return jsonify({"message": "Nessun dato disponibile"}), 404


if __name__ == '__main__':
    app.run(debug=True)
