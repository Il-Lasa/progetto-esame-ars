
# Webapp Qualità dell'Aria in Puglia

Questa webapp è progettata per monitorare la qualità dell'aria in diverse città della regione Puglia. 
L'applicazione consente di visualizzare le stazioni di monitoraggio su una mappa interattiva, consultare le misurazioni degli inquinanti per ogni stazione e confrontare i dati tra diverse stazioni e periodi. Include funzionalità di autenticazione per l'accesso agli utenti.

## Come eseguire l'applicazione

### Backend (Flask)

1. Andare nella cartella prototipo contenente il file `app.py`.
2. Installare l'environment conda con i pacchetti necessari:
   ```bash
   conda env create -f environment.yml
   ```
3. Avviare il server Flask con:
   ```bash
   python app.py
   ```
4. Il server sarà disponibile su `http://127.0.0.1:5000`.

### Frontend (React)

1. Andare nella cartella del progetto React (prototipo).
2. Installare le dipendenze con:
   ```bash
   npm install
   ```
3. Avviare l'applicazione con:
   ```bash
   npm run dev
   ```
4. Aprire l'app andando all'url indicato nel terminale.

## Funzionalità attuali

### 1. Visualizzazione delle stazioni di monitoraggio su una mappa interattiva

- La mappa interattiva utilizza **OpenStreetMap** tramite **React-Leaflet**.
- Le stazioni di monitoraggio della qualità dell'aria, prelevate da un database **SQLite** tramite **Flask**, sono rappresentate da marker.
- Cliccando sui marker della mappa, si possono vedere dettagli come la **denominazione**, il **comune** e la **provincia** della stazione.
- Sotto le informazioni della stazione è presente un pulsante **"Guarda informazioni"** che apre un modal con ulteriori dettagli e possibilità di visualizzare un grafico delle misurazioni.

### 2. Consultazione dei dati delle stazioni di monitoraggio

- **Modal Dettagli Stazione**: Premendo il pulsante "Guarda informazioni" su una stazione si apre un modal a schermo quasi intero che mostra:
  - Un grafico delle misurazioni nel tempo per un inquinante selezionato.
  - **Select** per filtrare i dati:
    - Inquinante (caricato dinamicamente dal backend).
    - Range di date (selezionabile tramite input di tipo data).
    - Stazione di confronto (opzionale) per confrontare i dati con un'altra stazione.

### 3. Dropdown per selezionare una stazione

- Il dropdown elenca tutte le stazioni di monitoraggio disponibili.
- Selezionando una stazione dal dropdown, il marker corrispondente viene evidenziato sulla mappa con la dimensione normale, mentre i marker delle altre stazioni vengono ridotti del 50%.

### 4. Funzionalità di autenticazione (Login e Registrazione)

- **Registrazione**: La schermata di registrazione richiede email, username, e password. I dati vengono salvati in un database separato con le password hashate.
- **Login**: La schermata di login consente l'accesso tramite email e password.
- **Logout**: È disponibile un pulsante di logout che rimuove il token di accesso dal frontend e reindirizza alla schermata di login.
  
### 5. Pagina Profilo

- La pagina del profilo mostra informazioni come **nome utente** e **email** dell'utente autenticato, con un pulsante per il logout.

### 6. Funzionalità di download e caricamento dati

- **Download Dati**: È disponibile un pulsante per scaricare i dati più recenti dal server ARPA, che vengono poi salvati nel database.
- **Modal di Notifica Download**: Dopo il download dei dati, l'utente viene informato con un modal che segnala l’esito del download (successo o dati già aggiornati).

### 7. Backend API con Flask e SQLAlchemy

- Il backend è sviluppato in **Flask** e utilizza **SQLAlchemy** per interagire con un database **SQLite** che contiene i dati relativi alle stazioni e alle misurazioni.
- Principali rotte API:
  - `/api/stations`: Restituisce l'elenco delle stazioni di monitoraggio con ID, denominazione, coordinate, comune, e provincia.
  - `/api/pollutants`: Restituisce l'elenco degli inquinanti disponibili.
  - `/api/station_measurements`: Restituisce i dati delle misurazioni per una stazione, un inquinante e un range di date specificati, con opzione per stazione di confronto.
  - `/api/register`: Gestisce la registrazione degli utenti.
  - `/api/login`: Gestisce l'autenticazione dell'utente e fornisce un token di accesso.

### Struttura del progetto

#### Frontend (React)

- **App.jsx**: Gestisce il routing dell'app e determina se l'utente è autenticato. Mostra la schermata di login/registrazione se non autenticato, altrimenti carica la **Home**.
- **Home.jsx**: Componente principale che mostra la mappa interattiva, il dropdown di selezione delle stazioni e i pulsanti per download e visualizzazione dei dati delle stazioni.
- **MapView.jsx**: Componente che gestisce la mappa e i marker delle stazioni. Cliccando su un marker si può visualizzare un popup con dettagli e un pulsante per accedere a ulteriori informazioni della stazione.
- **MeasurementModal.jsx**: Componente che gestisce il modal di dettaglio della stazione, con un grafico interattivo delle misurazioni filtrabile per inquinante, range di date e confronto opzionale con un'altra stazione.
- **Modal.jsx**: Componente che gestisce i popup di notifica per il download dei dati.
- **Login.jsx**: Componente per la schermata di login.
- **Register.jsx**: Componente per la schermata di registrazione.
- **Profile.jsx**: Mostra le informazioni dell'utente e fornisce un'opzione di logout.

#### Backend (Flask)

- **Flask** gestisce le richieste HTTP e comunica con il database **SQLite**.
- **SQLAlchemy** è utilizzato per gestire i modelli delle tabelle `stations`, `measurements`, `pollutants`, e `users`.
