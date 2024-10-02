
# Descrizione dell'App Qualità dell'Aria in Puglia

## Descrizione generale

L'applicazione permette di visualizzare le stazioni di monitoraggio della qualità dell'aria nella regione Puglia. Gli utenti possono interagire con una mappa interattiva per vedere le stazioni di monitoraggio, selezionare una stazione dal dropdown, e visualizzare informazioni dettagliate su ciascuna stazione.

## Funzionalità attuali

### 1. Mappa interattiva con marker delle stazioni
- La mappa mostra tutte le stazioni di monitoraggio presenti nel database. 
- Le stazioni sono rappresentate da marker interattivi: cliccando sui marker, vengono visualizzate informazioni come il nome della stazione, il comune e la provincia.

### 2. Dropdown di selezione della stazione
- L'utente può selezionare una stazione dal dropdown. Una volta selezionata, il marker della stazione scelta appare con la dimensione normale, mentre gli altri marker diventano più piccoli del 50%.

### 3. Backend API con Flask
- Il backend gestisce il database SQLite che contiene le informazioni sulle stazioni di monitoraggio.
- Flask espone un'API REST che fornisce i dati delle stazioni.

### 4. Gestione dei marker
- I marker delle stazioni sono visualizzati in base alle coordinate presenti nel database.
- Se una stazione è selezionata, il suo marker è visualizzato normalmente, mentre gli altri marker vengono ridotti in dimensione del 50%.

## Tecnologie utilizzate

- **React** per il frontend.
- **React-Leaflet** per la mappa interattiva.
- **Flask** per il backend e la gestione delle API.
- **SQLite** come database per le stazioni di monitoraggio.
- **Axios** per le richieste HTTP dal frontend al backend.

## Prossimi sviluppi

- Integrazione dei dati relativi agli inquinanti atmosferici.
- Implementazione di filtri avanzati per la visualizzazione dei dati sulla mappa.
