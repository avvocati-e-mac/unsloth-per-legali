# API e MCP

Sono due porte con direzioni diverse. L'**API** permette a un programma di fare una domanda al modello caricato. Un **MCP** offre al modello strumenti che può chiedere di usare, per esempio una ricerca. Nel [webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) la seconda porta ha funzionato, ma una citazione è stata riportata male.

| Collegamento | Chi lo usa | Esempio per uno studio |
| --- | --- | --- |
| **API** | Uno script o un'app chiama il modello | Inviare una pagina inventata a Vision e ricevere testo OCR. |
| **MCP** | Il modello chiede a uno strumento un'operazione | Cercare in una banca dati e poi aprire il provvedimento indicato. |

## API: documentata e provata per l'OCR

La [documentazione ufficiale Unsloth](https://unsloth.ai/docs/basics/api) descrive `/v1/chat/completions`, `/v1/models` e la creazione di chiavi da **Settings → API**. **Provato nel laboratorio:** uno script OCR ha chiamato l'API di Studio `2026.9.4` e il profilo attivo è stato letto dagli endpoint di stato. Questo non garantisce che opzioni e interfaccia restino identiche nelle versioni successive.

La chiave API è una password: conservala fuori dal repository, dagli esempi e dagli screenshot.

## MCP: valore e limite della dimostrazione

La build Desktop esaminata espone gestione e importazione dei server. **Verificato sul codice, non collaudato in esecuzione nel laboratorio:** il trasporto locale `stdio` può avviare un processo con i permessi dell'utente del backend; anche **Test connection** lo avvia. L'attivazione locale resta sospesa dopo una verifica d'integrità del bundle Desktop non superata. La [roadmap](../ROADMAP.md) prevede prima il ripristino, poi prove sintetiche in sola lettura.

Una chiamata allo strumento **non certifica** la risposta. Nei test RAG/OCR del laboratorio gli MCP remoti restano **Off**; nelle prove sintetiche dedicate al massimo **Ask**, con controllo del risultato alla fonte. Non copiare in guide pubbliche token, comandi o indirizzi operativi personali.
