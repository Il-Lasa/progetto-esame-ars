from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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

if __name__ == '__main__':
    app.run(debug=True)
