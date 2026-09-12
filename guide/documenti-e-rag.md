# Documenti e RAG

La [Chat di Unsloth](https://unsloth.ai/docs/new/studio/chat) permette di allegare file. Il **RAG** è un percorso diverso: prepara un indice dei documenti e, a ogni domanda, cerca i passaggi da consegnare al modello. Nell’[articolo del webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) lo paragono a un bibliotecario: è utile solo se trova il libro e la pagina giusti.

## Quale percorso serve?

| Hai… | Percorso | Controllo decisivo |
| --- | --- | --- |
| Una breve nota testuale | Allegato in Chat | Verifica che il testo letto corrisponda alla nota. |
| Molti documenti da interrogare più volte | RAG | Apri file e passaggio recuperati, non solo la risposta. |
| Un PDF composto da immagini | Vision/OCR prima del testo | Controlla date e cifre sulla pagina originale. [Guida OCR →](vision-e-ocr.md) |

**Verificato sul codice della build esaminata:** il PDF allegato direttamente in Chat segue un'estrazione testuale; una scansione senza testo non diventa automaticamente immagine per Vision. Nel RAG, PDF e DOCX usano parser distinti. Tabelle, note, intestazioni e posizione sulla pagina possono perdersi. Questo descrive l'implementazione letta, **non un collaudo completo** della pipeline reale.

## Un esperimento da fare con note inventate

Prepara **D01** e **D02** con date fittizie diverse e una parola unica in ciascuna. Chiedi quale documento sostiene una data. Poi:

1. apri il file e il passaggio citato;
2. riformula la domanda e controlla se il recupero cambia;
3. verifica che cosa resta nell'indice dopo la cancellazione.

È una **procedura proposta**. I test RAG end-to-end di Studio, compresi isolamento e cancellazione, sono ancora nella [roadmap](../ROADMAP.md).

Una raccolta separata per pratica non è una barriera di sicurezza già dimostrata. Questo progetto usa solo materiali sintetici. Durante prove RAG/OCR gli MCP remoti devono restare **Off**: un provider o strumento remoto può ricevere contenuti del turno anche quando modello e indice sono locali.
