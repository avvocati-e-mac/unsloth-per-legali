# Chat e finestra di contesto

Il **contesto** è il piano di lavoro del modello: istruzioni, messaggi precedenti, allegati e spazio per la risposta. Si misura in *token*, frammenti di testo che non corrispondono a un numero fisso di parole o pagine. La [guida Chat di Unsloth](https://unsloth.ai/docs/new/studio/chat) documenta allegati e impostazioni.

## Impostato, occupato, compreso: tre cose diverse

| Nella prova Qwen3.8 27B | Valore osservato | Significato |
| --- | ---: | --- |
| Contesto testuale caricato in Studio `2026.9.4` | 81.920 token | **Capienza configurata** con Vision spenta; non testo letto in quella richiesta. |
| Prompt della prova di scrittura | 1.697 token | **Testo realmente inviato** nella prova. |
| Risposta completa | 5.389 token | **Testo generato**, non garanzia di fedeltà ai documenti. |

Il modello era Qwen3.8 27B `UD-Q3_K_XL`, con un solo slot e cache KV `q4_0`. Su Studio `2026.9.2`, un prompt di 94.830 token è riuscito **solo dopo** timeout del primo tentativo e riuso del prefisso. Non trasferire quel risultato alla build più recente. [Metodo e limiti](../risultati/modelli.md).

## Una verifica proposta

Con solo testo **inventato**, scrivi tre fatti marcati «inizio», «centro» e «fine» e aggiungi frasi simili ma false. Chiedi: «Riporta i tre fatti e il punto esatto da cui provengono; se manca una fonte, dillo». Controlla:

1. quanti token sono stati davvero accettati;
2. se il fatto centrale è stato recuperato senza confonderlo con l'esca;
3. tempo al primo testo, omissioni e riferimenti inventati.

Questo è un **metodo proposto**, non una prova già eseguita qui.

Se una risposta si interrompe, guarda il motivo di arresto e il limite di output. Nel laboratorio **4.096 token** hanno troncato una richiesta; un tetto di **12.000** ha permesso di generare **5.389** token. Il tetto è spazio disponibile, non testo prodotto né qualità garantita.
