# Chat e finestra di contesto

La finestra di contesto è lo spazio che il modello usa per leggere istruzioni, cronologia, allegati e risposta. Il numero impostato non è una promessa di qualità: un testo lungo può entrare nella finestra e tuttavia essere letto male o richiedere molto tempo per il primo token. La [guida Chat di Unsloth](https://unsloth.ai/docs/new/studio/chat) spiega allegati e impostazioni correnti.

**Provato nel laboratorio:** con Qwen3.8 27B `UD-Q3_K_XL`, Vision disattivata, un solo slot e cache KV `q4_0`, Studio `2026.9.4` ha caricato un profilo testuale da **81.920 token**. Il test di scrittura ha usato però solo **1.697 token di prompt**: la risposta completa è stata di 5.389 token. Non dimostra che si possa riempire quasi tutta la finestra e ottenere anche una risposta lunga. Su una build precedente un prompt da 94.830 token è riuscito solo dopo un primo tentativo scaduto e il riuso del prefisso. [Dettagli e versioni](../risultati/modelli.md).

Per una prova personale con testo **sintetico**, prepara tre brevi fatti marcati «inizio», «centro» e «fine», aggiungi frasi simili ma false, e chiedi al modello di riportare solo i tre fatti con il punto da cui provengono. Annota il contesto configurato, i token realmente accettati, il tempo al primo testo e gli errori. Questo è un **metodo proposto**, non un test eseguito da questa guida.

Se la risposta si interrompe, guarda il motivo di arresto e il budget di output. Nel laboratorio 4.096 token hanno troncato una richiesta sintetica; un tetto di 12.000 ha lasciato completare **5.389 token effettivi**. Aumentare il tetto non significa che il modello genererà 12.000 token né che migliorerà la qualità.
