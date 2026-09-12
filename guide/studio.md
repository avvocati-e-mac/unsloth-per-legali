# Come funziona Unsloth Studio

Studio è la **scrivania**: permette di scegliere e caricare un modello, conversare nella Chat e renderlo raggiungibile da programmi tramite API locale. Il modello è il **collaboratore** che produce testo. I documenti non diventano automaticamente conoscenza permanente del modello.

La [presentazione ufficiale di Studio](https://unsloth.ai/docs/new/studio) è il riferimento per installazione e versioni; la [guida Chat di Unsloth](https://unsloth.ai/docs/new/studio/chat) documenta modelli e allegati. Le voci dell'interfaccia possono cambiare.

## Un primo giro, con testo inventato

1. Scegli un modello compatibile con la memoria del tuo Mac; **prima del download** controlla formato e quantizzazione.
2. Dopo il caricamento, verifica quale **modello** e quale **contesto** risultano davvero attivi. Il nome di un preset non basta.
3. Prova una domanda innocua: «Riassumi in tre punti: l'assemblea immaginaria si terrà il 14 ottobre 2042».
4. Confronta la risposta con la frase di partenza. Se compare una sede o un orario, è un'aggiunta senza fonte.

Questi passi sono un **esercizio proposto**. Non rappresentano un nuovo collaudo della procedura.

## Che cosa è stato provato qui

Su Mac Studio M1 Max e Studio `2026.9.4`, il laboratorio ha caricato Qwen3.8 27B GGUF quantizzato e salvato due preset, poi riletti. Le misure dipendono da versione e memoria libera: [configurazione, risultati e limiti](../risultati/modelli.md).

Desktop e CLI possono usare lo **stesso ambiente**. Prima di intervenire su un modello che sembra già attivo, controlla lo stato. Download, aggiornamenti e accesso dalla rete richiedono valutazioni operative distinte.
