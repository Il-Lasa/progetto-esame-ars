
# Webapp Qualità dell'Aria in Puglia

Questa webapp è progettata per monitorare la qualità dell'aria in diverse città della regione Puglia. Attualmente l'app mostra le stazioni di monitoraggio su una mappa interattiva e permette di selezionare una stazione dal dropdown per evidenziarla.

## Funzionalità attuali

### 1. Visualizzazione delle stazioni di monitoraggio su una mappa interattiva
- La mappa interattiva utilizza **OpenStreetMap** tramite **React-Leaflet**.
- Le stazioni di monitoraggio della qualità dell'aria, prelevate da un database **SQLite** tramite **Flask**, sono rappresentate da marker.
- Cliccando sui marker della mappa, si possono vedere dettagli come la **denominazione**, il **comune** e la **provincia** della stazione.

### 2. Dropdown per selezionare una stazione
- Il dropdown elenca tutte le stazioni di monitoraggio disponibili.
- Selezionando una stazione dal dropdown, il marker corrispondente viene evidenziato sulla mappa con la dimensione normale, mentre i marker delle altre stazioni vengono ridotti del 50%.

### 3. Backend API con Flask e SQLAlchemy
- Il backend è sviluppato in **Flask** e utilizza **SQLAlchemy** per interagire con un database **SQLite** che contiene i dati relativi alle stazioni.
- Due rotte API principali:
  - `/api/stations`: Restituisce l'elenco delle stazioni di monitoraggio con ID, denominazione, coordinate, comune, e provincia.
  
### Struttura del progetto

#### Frontend (React)
- **App.jsx**: Componente principale che gestisce il layout della pagina, il dropdown di selezione delle stazioni e la visualizzazione della mappa.
- **MapView.jsx**: Componente che gestisce la mappa e i marker. I marker delle stazioni non selezionate sono ridotti del 50% rispetto al marker della stazione selezionata.
  
#### Backend (Flask)
- **Flask** gestisce le richieste HTTP e comunica con il database **SQLite**.
- **SQLAlchemy** è utilizzato per gestire i modelli e le query SQL.
- Gestione delle richieste API tramite **CORS**.

## Come eseguire l'applicazione

### Backend (Flask)
1. Vai nella cartella contenente il file `app.py`.
2. Installa le dipendenze con:
   ```bash
   pip install Flask Flask-SQLAlchemy flask-cors
   ```
3. Avvia il server Flask con:
   ```bash
   python app.py
   ```
4. Il server sarà disponibile su `http://127.0.0.1:5000`.

### Frontend (React)
1. Vai nella cartella del progetto React.
2. Installa le dipendenze con:
   ```bash
   npm install
   ```
3. Avvia l'applicazione con:
   ```bash
   npm run dev
   ```
4. L'app sarà disponibile su `http://localhost:3000`.

## Prossimi passi
1. **Integrazione dei dati di misurazione degli inquinanti**: Sviluppare la rotta API per ottenere i dati degli inquinanti e visualizzarli.
2. **Miglioramento della visualizzazione**: Possibilità di filtrare le stazioni per comune o per inquinante monitorato.
