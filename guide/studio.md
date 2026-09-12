# Come funziona Unsloth Studio

**Documentato da Unsloth e osservato nel laboratorio.** Studio riunisce interfaccia, caricamento del modello, Chat e API locale. La [guida ufficiale](https://unsloth.ai/docs/new/studio) è il riferimento per installazione e versioni aggiornate; [la pagina Chat](https://unsloth.ai/docs/new/studio/chat) descrive modelli e allegati. Le voci dell'interfaccia possono cambiare fra release.

Per un primo orientamento, apri Studio, scegli un modello che rientri nella memoria della macchina e controlla formato e quantizzazione prima del download. Dopo il caricamento, verifica nella schermata di stato quale modello e quale finestra di contesto sono davvero attivi. Solo allora prova una richiesta innocua, per esempio: «Riassumi in tre punti questo testo inventato: l'assemblea si terrà il 14 ottobre 2042». Non leggere un nome di preset come prova che il runtime abbia applicato quei parametri.

**Provato nel laboratorio:** sul Mac Studio M1 Max un Qwen3.8 27B GGUF quantizzato è stato caricato nella build Studio `2026.9.4`; due preset distinti sono stati salvati e riletti. I risultati dipendono dalla memoria libera e dalla versione. [Misure e limiti](../risultati/modelli.md).

L'interfaccia Desktop e la CLI possono usare lo stesso ambiente. Se un modello sembra già in esecuzione, controlla lo stato prima di avviare altre operazioni. Download, aggiornamenti e impostazioni di rete sono decisioni operative separate dalla lettura di questa guida.
