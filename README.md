# IA locale per avvocati: dalla demo alle prove

*Unsloth Studio sul Mac, spiegato attraverso documenti, domande ed errori che un avvocato riconosce.*

Può un Mac aiutarmi a leggere una scansione, ritrovare un fatto e preparare una bozza? È la domanda da cui è nato il [webinar per la Camera Civile di Ravenna](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/). Qui proseguo il lavoro nello spirito di [**Avvocati e Mac**](https://www.avvocati-e-mac.it/): spiego come funziona il sistema, provo ciò che posso misurare e mostro anche gli errori.

**L’idea in una frase:** Unsloth Studio fa girare un modello sul computer e gli offre una Chat; documenti e strumenti possono entrare nella conversazione attraverso percorsi diversi. Il modello **non è una banca dati giuridica**: produce testo, che diventa utile solo se sappiamo da quali carte e fonti proviene. Studio è ancora presentato da Unsloth come **beta**: nomi e passaggi dell’interfaccia possono cambiare.

> [!NOTE]
> **Tre etichette da tenere a mente.** *Provato* significa eseguito nel laboratorio con dati sintetici; *mostrato* indica la demo raccontata nel webinar; *documentato* descrive una funzione o un metodo, senza dichiarare che sia stato collaudato qui. Le misure valgono per la configurazione indicata, non per ogni Mac.

## La scrivania, il collaboratore e le carte

1. **Il Mac ospita il modello.** Pensa al modello come a un collaboratore che sa scrivere, ma non ha letto il tuo fascicolo. Per far entrare modelli grandi nella memoria si usano spesso versioni *quantizzate*: come una copia più leggera di un volume illustrato, occupano meno spazio ma possono perdere dettagli. La [documentazione di Unsloth Studio](https://unsloth.ai/docs/new/studio) indica **Desktop** come punto di partenza su Mac. [Come orientarsi in Studio →](guide/studio.md)

2. **La Chat è il colloquio.** Scrivi una domanda, eventualmente alleghi un file, ricevi una risposta. Il *contesto* è il piano di lavoro su cui stanno istruzioni, conversazione, testo allegato e spazio per la risposta. I *token* sono frammenti di testo, non pagine: una finestra impostata a 80K token non prova che il modello abbia letto bene 80K token. La [guida ufficiale Chat](https://unsloth.ai/docs/new/studio/chat) documenta allegati e impostazioni. [Chat e contesto →](guide/chat-e-contesto.md)

3. **Le carte entrano in modi diversi.** Un PDF testuale allegato porta il suo testo alla conversazione. Il **RAG fa da bibliotecario**: indicizza molti documenti e seleziona passaggi per una domanda; il suo percorso completo in Studio resta da collaudare. Una scansione, invece, è un’immagine: serve Vision/OCR per estrarne testo. Nella build esaminata, allegare un PDF scansito alla Chat **non** invia automaticamente le pagine a Vision. [Documenti e RAG →](guide/documenti-e-rag.md) · [Vision e OCR →](guide/vision-e-ocr.md)

4. **Gli strumenti sono collegamenti, non conoscenza incorporata.** Con l’**API** un programma parla al modello; con un **MCP** il modello può chiedere a uno strumento di fare un’operazione, per esempio una ricerca. La [documentazione API di Unsloth](https://unsloth.ai/docs/basics/api) descrive il primo collegamento; il [webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) mostra il secondo, compreso un errore di citazione. [API e MCP →](guide/api-e-mcp.md)

### Un esempio, prima di parlare di benchmark

Immagina due note **inventate**: **D01** dice «richiesta ricevuta il 12 ottobre 2042»; **D02** dice «risposta inviata il 16 ottobre 2042».

- **Con due note**, puoi chiedere in Chat: «Quando è stata inviata la risposta? Indica la nota e riporta il passaggio». Devi trovare **16 ottobre in D02**, non una data plausibile.
- **Con centinaia di note**, un RAG dovrebbe trovare D02 prima di porre la domanda al modello. Se il bibliotecario recupera D01, il risultato può essere sbagliato: controlla il file e il passaggio indicati.
- **Se D02 è una scansione**, prima verifica che l’OCR abbia letto *16* e non *18*. Il testo plausibile non sostituisce la pagina originale.

È un **esercizio proposto**, non una prova eseguita qui. La [guida all’uso legale](guide/uso-legale-e-limiti.md) offre una lista di controlli per bozze e citazioni.

## Che cosa ho provato davvero

### Qwen3.8 27B — laboratorio

- **Visto:** con Studio `2026.9.4` sul Mac dei test ho caricato un profilo testo da **81.920 token** e uno Vision da **16.384**. Qwen ha completato una risposta sintetica di **5.389 token** e trascritto due pagine inventate con errori puntuali.
- **Limite:** quella risposta partiva da **1.697 token di input**; non prova un atto lungo scritto dopo aver letto 80K token di documenti. In una bozza legale sintetica il modello ha aggiunto dati e omesso un importo.

### Gemma 4 12B — webinar

- **Mostrato:** nell’[articolo sul webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) descrivo una demo più rapida, con chiamate agli strumenti riuscite e contesto più ampio.
- **Limite:** nel flusso giuridico una citazione è stata riportata male. Mancano in questo repository prompt, tempi e output per un confronto numerico riproducibile con Qwen.

### Gemma 4 26B-A4B MoE — prima misura locale

- **Visto:** con circa **30K token di input sintetico**, MLX ha generato a **36,8 token/s** e GGUF a **13,8 token/s**. È una sola esecuzione per backend, con pacchetti e runtime diversi.
- **Limite:** MLX ha inventato riferimenti a righe e raggiunto un margine di memoria ridotto. Nessuno dei due formati ha dimostrato **90K di input** lasciando spazio a una risposta lunga.

Configurazioni, metodo, tempi e limiti sono nella [scheda **Modelli e risultati**](risultati/modelli.md). Le verifiche ancora aperte sono nella [roadmap](ROADMAP.md), senza scadenze promesse.

## Il Mac dietro i numeri

|  | Mac Studio **M1 Max** dei test | Mac Studio **M5 Max base** |
| --- | --- | --- |
| Memoria unificata | 32 GB | 36 GB |
| GPU | 24 core | 32 core |
| Banda dichiarata | 400 GB/s | 460 GB/s |

Il primo è la macchina usata nel [webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/); per il secondo riporto la [scheda Apple](https://www.apple.com/it/mac-studio/specs/). **Non ho eseguito gli stessi test sui due Mac.** La banda di memoria è una caratteristica dell’hardware, non un numero di token al secondo: modello, quantizzazione, contesto e memoria libera cambiano il risultato.

> [!WARNING]
> **Locale non significa automaticamente «tutto resta sul Mac».** Ricerca web, provider esterni e MCP possono inviare contenuti fuori dal computer. Parti da testi inventati e verifica sempre documenti e citazioni. Questo progetto non contiene documenti di clienti o corpus di pratiche, nemmeno anonimizzati.

Questo repository è indipendente da Unsloth. La [documentazione ufficiale dell’API](https://unsloth.ai/docs/basics/api) descrive il collegamento ai programmi esterni; qui trovi anche lo [script OCR revisionato](scripts/ocr-pdf-qwen38-api.py) con [test offline](tests/test_ocr_pdf.py). Guide e risultati sono in [CC BY 4.0](LICENSE.md), codice e test in [MIT](LICENSE.md).
