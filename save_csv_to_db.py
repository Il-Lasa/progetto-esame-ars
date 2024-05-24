import sqlite3
import pandas as pd
import sys

numero_colonne = 26
numero_righe = 311

conn = sqlite3.connect('arpa.db')
cursor = conn.cursor()

csv_file = sys.argv[1]
df = pd.read_csv(csv_file)

print("--------------- INFO CSV INSERITO ---------------")
print(f'Numero di colonne: {len(df.columns)} / {numero_colonne}')
print(f'Numero di righe: {len(df)} / {numero_righe}')
data = df['properties.data_di_misurazione'].unique()
print(f'Data di misurazione: {data}')
print("-------------------------------------------------")
# # Inserimento di nuove stazioni
# for _, row in df.iterrows():
#     cursor.execute('''
#     INSERT OR IGNORE INTO stations (
#         id_station, denominazione, coordinates, rete, interesse_rete,
#         tipologia_stazione, tipologia_area, comune, provincia, paese, paese_esteso
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (
#         row['properties.id_station'], row['properties.denominazione'], 
#         str(row['geometry.coordinates']), row['properties.rete'], 
#         row['properties.interesse_rete'], row['properties.tipologia_di_stazione'], 
#         row['properties.tipologia_di_area'], row['properties.comune'], 
#         row['properties.provincia'], row['properties.paese'], 
#         row['properties.paese_esteso']
#     ))

# # Inserimento di nuovi inquinanti
# for _, row in df.iterrows():
#     cursor.execute('''
#     INSERT OR IGNORE INTO pollutants (
#         inquinante_misurato, limite, unita_misura
#     ) VALUES (?, ?, ?)
#     ''', (
#         row['properties.inquinante_misurato'], row['properties.limite'], row['properties.unita_misura']
#     ))

# conn.commit()

# # Inserimento delle rilevazioni
# for _, row in df.iterrows():
#     cursor.execute('''
#     SELECT COUNT(*)
#     FROM measurements
#     WHERE data_rilevazione = ? AND inquinante_misurato = ? AND id_station = ?
#     ''', (row['properties.data_di_misurazione'], row['properties.inquinante_misurato'], row['properties.id_station']))
    
#     count = cursor.fetchone()[0]
    
#     if count == 0:
#         cursor.execute('''
#         INSERT INTO measurements (
#             data_rilevazione, inquinante_misurato, id_station, 
#             valore_inquinante_misurato, superamenti, indice_qualita, 
#             responsabile_dato, punto_di_contatto, sorgente, marker_color
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             row['properties.data_di_misurazione'], row['properties.inquinante_misurato'], 
#             row['properties.id_station'], row['properties.valore_inquinante_misurato'], 
#             row['properties.superamenti'], row['properties.indice_qualita'], 
#             row['properties.responsabile_dato'], row['properties.punto_di_contatto'], 
#             row['properties.sorgente'], row['properties.marker-color']
#         ))

# conn.commit()
# conn.close()
# print("Dati inseriti nel database con successo")