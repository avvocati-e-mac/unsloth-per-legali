# Vision e OCR delle scansioni

**Vision** permette al modello di guardare un'immagine. **OCR** è il risultato che cerchiamo: testo ricavato dalla pagina, da confrontare con l'originale. Una trascrizione fluida può comunque cambiare una cifra. La [guida Chat di Unsloth](https://unsloth.ai/docs/new/studio/chat) documenta allegati immagine; la [guida API](https://unsloth.ai/docs/basics/api) documenta l'accesso da programmi.

## Il percorso provato

`PDF sintetico → PNG a 200 dpi → Qwen Vision via API → testo per pagina`

**Provato nel laboratorio:** Qwen3.8 27B, Vision attiva e contesto 16.384, ha trascritto **due pagine inventate**, una ruotata di 90°. La similarità delle sequenze di parole normalizzate rispetto al testo di riferimento è stata **0,9939** e **0,9816**; alcune parole e timbri erano errati. È una formula su due pagine, **non** un punteggio OCR generale. [Metodo e limiti →](../risultati/modelli.md)

## Come controllare una scansione

Con una pagina **inventata**, inserisci due date, un importo e una sigla. Conserva separatamente il testo corretto. Poi verifica:

1. ogni **campo critico** sulla pagina, non soltanto la somiglianza complessiva;
2. parole illeggibili, omissioni e parti aggiunte;
3. la pagina precisa che ha prodotto ogni trascrizione.

È una **procedura proposta**. Il PDF scansito allegato direttamente in Chat **non è stato collaudato**; nella build esaminata l'allegato PDF segue l'estrazione del testo, non l'invio delle pagine come immagini a Vision.

## Che cosa ottieni, e che cosa manca

Il percorso provato produce **file di testo e manifest**, non un PDF ricercabile con evidenziazioni allineate. Il testo libero non contiene coordinate di pagina: per un layer OCR fedele servono posizioni e controllo visivo.

Lo [script OCR](../scripts/ocr-pdf-qwen38-api.py) riproduce il percorso PDF → PNG → API → testo. Richiede Python 3.10+, Poppler (`pdfinfo`, `pdftoppm`), Studio su **`127.0.0.1:8888`** con Qwen Vision già caricato e la chiave ufficiale in `UNSLOTH_API_KEY`. Esempio con PDF **sintetico** fuori dal repository:

```bash
python3 scripts/ocr-pdf-qwen38-api.py /percorso/esterno/esempio.pdf --output /percorso/esterno/risultato-ocr
```

Controlla ogni `page-*.txt` contro l'originale. Lo script **non** carica modelli e **non** crea un layer OCR; è stato verificato offline con risposta API simulata. L'esecuzione reale descritta nella scheda dei risultati appartiene al laboratorio privato.
