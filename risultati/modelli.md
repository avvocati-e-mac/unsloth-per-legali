# Modelli: che cosa sappiamo davvero

Questa scheda distingue **fatti osservati nel laboratorio**, **inferenze** e **stime**. Le misure non sono benchmark universali né un confronto su hardware uguale. La macchina osservata è un Mac Studio M1 Max, 32 GB di memoria unificata, GPU a 24 core; salvo indicazione diversa, Studio è `2026.9.4`.

## Qwen3.8 27B — prove del laboratorio

**Fatti osservati.** Il GGUF `unsloth/Qwen3.8-27B-GGUF`, variante `UD-Q3_K_XL`, è stato usato con un solo slot, cache KV `q4_0` e speculative decoding spento. I preset salvati e riletti sono **Vision 16.384** e **testo senza Vision 81.920 token**. Il profilo 80K è stato caricato e confermato nello stato del runtime. Un prompt sintetico di 1.697 token ha prodotto 5.389 token di output (2.950 parole) con `finish_reason=stop` in 538,12 s nel retry con prefisso in cache. La prima richiesta, limitata a 4.096 token, era stata troncata. Una bozza preliminare di atto inventato ha prodotto 2.196 token, 1.114 parole, ma ha aggiunto dati non forniti e omesso un importo. Con Vision 16K, due pagine sintetiche inviate via API come PNG hanno prodotto similarità di parole normalizzate 0,9939 e 0,9816 rispetto al gold; erano presenti errori puntuali.

Su Studio `2026.9.2`, con Vision spenta, un prompt di 65.510 token ha completato 16 token di output. Un prompt di 94.830 token ha completato 64 token **solo al retry dopo timeout del tentativo freddo**, con prefisso in cache. Su `2026.9.4` è stato confermato il caricamento di 81.920 token, **non** una generazione con prompt quasi pieno e risposta lunga.

**Inferenze.** Il contesto utilizzabile dipende dalla memoria disponibile, dal profilo e dalla build. I preset condividono lo stesso file del modello ma richiedono verifica dello stato effettivo dopo il caricamento. La bozza e l'OCR richiedono confronto con originali e fonti.

**Stime.** Dividendo token di risposta per durata totale delle tre chiamate di scrittura si ottengono circa 9,7–10,0 token/s apparenti. Presupposto: quelle sole chiamate, con cache diversa fra prima richiesta e retry; incertezza alta per altri prompt e contesti. Il limite di output impostato a 12.000 è una capienza, non una misura di 12.000 token generati.

**Metodo OCR.** Il PDF sintetico è stato renderizzato a 200 dpi. Il gold era la trascrizione integrale della pagina; il testo OCR è stato ritagliato dal primo «Capitolo» al primo footer, poi entrambi sono stati tokenizzati con `re.findall(r'[\w@.<>-]+', testo.lower())` e confrontati con `difflib.SequenceMatcher(autojunk=False).ratio()`. Le sequenze avevano 163 token ciascuna. Questa formula non è CER, WER né una valutazione del layout. Non è stato creato un PDF con layer OCR.

## Gemma 4 12B — dimostrazione nel webinar

**Fatti riportati dall'autore.** Nell'[articolo sul webinar del 3 settembre 2026](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) Gemma 4 12B è descritta come più rapida di Qwen nella demo, capace di un contesto più ampio e di chiamare gli strumenti. Nello stesso flusso giuridico ha **riportato male una citazione**. Nel repository non sono disponibili prompt, output, configurazione completa e tempi necessari a un confronto numerico riproducibile. «Più rapida» e «contesto più ampio» restano osservazioni della dimostrazione, non misure qui confrontabili.

## Gemma 4 26B-A4B MoE — da collaudare

**Fatti osservati.** Sono stati scaricati e verificati localmente il GGUF QAT Unsloth `UD-Q4_K_XL` (14.249.047.104 byte, SHA-256 `a7c5bc715f5ff8e99a3e8901ce7d2b42b402c669bf24f7c5250747633d0f5891`) e il checkpoint MLX QAT di mlx-community (12 file, 15.641.241.228 byte; shard verificati). Sono artefatti **diversi**, conservati fuori da Git. [Albero GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF/tree/7b92b5b28818151e8669af2e45e88d6086f490dd) e [albero MLX](https://huggingface.co/mlx-community/gemma-4-26B-A4B-it-qat-4bit/tree/0e3cbab38ce568cf6e23543010d08d03b731910c).

**Inferenza.** La presenza dei pesi non prova che Studio li carichi o che un contesto lungo sia utilizzabile. **Nessun risultato locale di inferenza Gemma MoE è stato acquisito.** Non pubblichiamo velocità attese: le stime da altri runtime e quantizzazioni sono troppo incerte per guidare questa scelta. Il collaudo è descritto nella [roadmap](../ROADMAP.md).
