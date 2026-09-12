# API e MCP

L'**API** permette a un programma di parlare con il modello caricato. Un **MCP** permette al modello di chiedere a uno strumento di fare un'operazione, per esempio cercare in una banca dati. Sono due collegamenti diversi, con permessi e rischi diversi.

La [documentazione ufficiale dell'API Unsloth](https://unsloth.ai/docs/basics/api) descrive l'endpoint locale OpenAI-compatible `/v1/chat/completions`, l'elenco `/v1/models` e le chiavi create da **Settings → API**. **Provato nel laboratorio:** lo script locale di OCR ha chiamato l'API sulla build `2026.9.4`; il profilo attivo è stato letto tramite gli endpoint di stato. Questo non dimostra che ogni opzione resti invariata nelle versioni successive. Conserva la chiave fuori dal repository e non copiarla in esempi, screenshot o log.

Per gli MCP, la build Desktop esaminata espone gestione, importazione e controllo dei server. **Verificato sul codice, non collaudato in esecuzione:** il trasporto locale `stdio` può avviare un processo con i permessi dell'utente del backend; `Test connection` lo avvia davvero. Nel laboratorio l'attivazione è sospesa perché una verifica d'integrità del bundle Desktop non è passata. La [roadmap](../ROADMAP.md) richiede prima il ripristino e poi test sintetici read-only. Non pubblicare comandi locali, token o endpoint operativi come se fossero impostazioni universali.

Nel [webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) un MCP ha mostrato il valore pratico della ricerca giuridica, ma anche un errore di citazione. Una tool call riuscita non certifica la risposta. Quando fai prove RAG o OCR, spegni gli MCP remoti; nei test sintetici dedicati chiedi approvazione per ciascuna chiamata e controlla il risultato alla fonte.
