import sqlite3

conn = sqlite3.connect('arpa.db')
cursor = conn.cursor()

# Creazione della tabella stations
cursor.execute('''
  CREATE TABLE IF NOT EXISTS stations (
    id_station TEXT PRIMARY KEY,
    denominazione TEXT,
    coordinates TEXT,
    rete TEXT,
    interesse_rete TEXT,
    tipologia_stazione TEXT,
    tipologia_area TEXT,
    comune TEXT,
    provincia TEXT,
    paese TEXT,
    paese_esteso TEXT
  )
''')

# Creazione della tabella pollutants
cursor.execute('''
  CREATE TABLE IF NOT EXISTS pollutants (
    inquinante_misurato TEXT PRIMARY KEY,
    limite REAL,
    unita_misura TEXT
  )
''')

# Creazione della tabella measurements
cursor.execute('''
  CREATE TABLE IF NOT EXISTS measurements (
    data_rilevazione TEXT,
    inquinante_misurato TEXT,
    id_station TEXT,
    valore_inquinante_misurato REAL,
    superamenti INTEGER,
    indice_qualita REAL,
    responsabile_dato TEXT,
    punto_di_contatto TEXT,
    sorgente TEXT,
    marker_color TEXT,
    FOREIGN KEY (id_station) REFERENCES stations (id_station),
    FOREIGN KEY (inquinante_misurato) REFERENCES pollutants (inquinante_misurato)
  )
''')

conn.commit()
conn.close()