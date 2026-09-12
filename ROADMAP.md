# Roadmap delle verifiche

Stato al 12 settembre 2026. Le attività non hanno una scadenza promessa. «Da fare» indica una domanda aperta, non un'autorizzazione ad avviare Studio, caricare modelli, inviare prompt o modificare configurazioni.

| Attività | Stato | Criterio di completamento |
|---|---|---|
| Ricostruire la prova Gemma 4 12B del webinar | Da documentare | Registrare artefatto e quantizzazione, build, prompt sintetici, tool, contesto effettivo, tempi, output e verifica delle citazioni; separare ricordo della demo e misure riproducibili. |
| Collaudare Gemma 4 26B-A4B MoE | Artefatti GGUF e MLX presenti, inferenza non acquisita | Per ciascun backend: caricamento e stato verificati, prompt realmente occupati a più lunghezze, richiamo di fatti a inizio/centro/fine, tempi a freddo e con cache, memoria e swap; tre esecuzioni stabili al massimo candidato. |
| Ampliare la valutazione OCR | Due pagine sintetiche provate via API Vision | Almeno 30 pagine sintetiche con trascrizione gold, casi ruotati e degradati; CER, WER, omissioni, testo inventato ed esattezza dei campi critici, confrontati con OCR tradizionale. |
| Provare il RAG nella pipeline reale di Studio | Piano e corpus sintetici, gate E2E aperti | Verificare parser/OCR, embedding e pooling, indice, recupero, citazioni, isolamento e cancellazione nella build effettiva; misurare ogni fase separatamente. Un harness esterno resta diagnostico. |
| Verificare MCP e chiamate agli strumenti | Supporto della build documentato; prova completa assente | Ripristinare e verificare integrità dell'app, poi test sintetici read-only con autorizzazioni esplicite, output grezzo, citazioni e assenza di chiamate non richieste. MCP remoti Off durante RAG/OCR. |
| Valutare bozze legali sintetiche | Una bozza preliminare Qwen esaminata | Casi e rubriche preregistrati: fatti, documenti, segnaposto, importi, fonti e omissioni; revisione umana indipendente e misura degli errori critici. |
| Routing fra più modelli | Successivo, solo disegno | Considerarlo dopo misure affidabili su qualità, tempo di cambio modello, contesto conservato e tool; documentare recupero in caso di fallimento. |
| Fine-tuning | Successivo, non avviato | Valutarlo solo se prompt, template, strumenti e RAG mostrano un difetto ripetibile e un holdout dimostra miglioramento senza regressioni critiche. |

Per le misure già disponibili e i loro confini: [modelli e risultati](risultati/modelli.md).
