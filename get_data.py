import requests
import pandas as pd
import datetime
import sys

url = "http://old.arpa.puglia.it/ARPA_ARIA/dati.jsp?format=GeoJSON"

print(f"Prendendo i dati da {url}")
try:
  response = requests.get(url)
  data = response.json()
  if data:
    print("Dati recuperati con successo")
    print("-"*15)
    print("Creazione del dataframe")
    
    features = data['features']

    df = pd.json_normalize(features)

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    print("Dataframe creato con successo")
    
    print("Esportazione del dataframe come CSV in corso...")
    df.to_csv(f'{today_str}_arpa_aria.csv', index=False)
    print(f"CSV esportato in {today_str}_arpa_aria.csv")
    
except Exception as e:
  print("Errore nel recupero dei dati")
  print(f"Errore durante la richiesta HTTP: {e}")
  sys.exit(1)
