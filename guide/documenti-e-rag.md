# Documenti e RAG

Un allegato in Chat e una raccolta indicizzata rispondono a esigenze diverse. L'allegato aggiunge contenuto al turno; il RAG suddivide i documenti, cerca passaggi pertinenti e li porta al modello quando fai una domanda. La [guida ufficiale della Chat](https://unsloth.ai/docs/new/studio/chat) conferma gli allegati; l'[articolo del webinar](https://www.avvocati-e-mac.it/blog/2026/09/03/ia-locale-per-avvocati-camera-civile-ravenna/) introduce il RAG con esempi per avvocati.

**Verificato sul codice della build esaminata:** l'allegato PDF in Chat segue un'estrazione testuale; un PDF scansito senza testo non diventa automaticamente un'immagine per Vision. Nel RAG della build esaminata PDF e DOCX passano per parser distinti; tabelle, note, intestazioni e pagine possono perdere informazioni o posizione. Queste osservazioni descrivono l'implementazione letta, **non** un collaudo completo di ogni file o della versione futura.

Per capire che cosa recupera un indice, usa solo documenti inventati: ad esempio due note con date fittizie diverse, ciascuna con una parola chiave unica. Chiedi quale nota sostiene una data e apri il file e il passaggio indicati. Ripeti con la domanda riformulata, poi verifica cosa resta dopo la cancellazione. È una **procedura di verifica proposta**; i test RAG end-to-end nella pipeline reale di Studio sono ancora nella [roadmap](../ROADMAP.md).

Una «knowledge base per pratica» aiuta a organizzare il lavoro, ma non va scambiata per una barriera di sicurezza già dimostrata. In questo repository non entrano documenti o corpus reali, nemmeno anonimizzati. Nei test RAG/OCR del laboratorio gli MCP remoti restano Off. Anche se modello e indice sono locali, un provider o un tool remoto può ricevere contenuti del turno.
