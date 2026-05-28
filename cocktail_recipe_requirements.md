# Requisiti Progetto Cocktail Recipe
Progetto: CocktailBook (ispirato al layout di RecipeHub)
Versione documento: 1.0
Ultimo aggiornamento: 2026-05-05

## 1. Panoramica del Progetto
Realizzare un'applicazione digitale di ricette di cocktail che permetta agli utenti di scoprire, salvare, personalizzare e condividere ricette. Supportare la navigazione per ingredienti, tecniche, bicchieri, profilo di gusto e occasione.

## 2. Obiettivi
- Fornire un catalogo di ricette ricercabile e filtrabile.
- Permettere agli utenti di salvare i preferiti, creare collezioni e inviare ricette.
- Offrire il dosaggio preciso degli ingredienti, istruzioni passo-passo e contenuti visivi.
- Supportare la visualizzazione offline delle ricette salvate e la sincronizzazione multi-dispositivo.

## 3. Ambito
In ambito:
- CRUD delle ricette per utenti e amministratori.
- Analisi degli ingredienti e conversione delle unità di misura (metrico/imperiale).
- Account utente, autenticazione e impostazioni del profilo.
- Navigazione, ricerca, filtri e raccomandazioni.
- Valutazioni, commenti e condivisione social.
Fuori ambito (fase 1):
- Acquisto di alcolici in-app o hardware per la verifica dell'età.
- Istruzioni video in diretta per la preparazione.

## 4. Profili Utente
- Appassionato casalingo: cerca ricette, salva i preferiti, segue i creatori.
- Barman professionista: invia ricette avanzate, aggiunge tag alle tecniche.
- Ospite occasionale: visualizza le ricette e le condivide tramite link social.
- Amministratore: modera i contenuti, gestisce le categorie e le segnalazioni.

## 5. Funzionalità Principali
- Scheda ricetta: titolo, autore, foto, ingredienti (quantità), passaggi, tempo di preparazione, difficoltà, tag, tipo di bicchiere, guarnizione, stima ABV.
- Dosaggio degli ingredienti: regolazione delle porzioni e delle unità di misura.
- Ricerca e filtri: testo libero, inclusione/esclusione di ingredienti, profilo di gusto, difficoltà, tempo.
- Collezioni e preferiti: liste private/pubbliche.
- Flusso di invio/modifica: bozza, validazione, coda di moderazione.
- Supporto offline: cache delle ricette salvate.
- Social: link di condivisione, esportazione ricetta stampabile.
- Analisi: ricette popolari, tendenze.

## 6. Storie Utente (esempi)
- Da utente voglio cercare per ingrediente così posso trovare i cocktail che posso preparare adesso.
- Da utente voglio scalare le quantità degli ingredienti così posso preparare qualsiasi numero di porzioni.
- Da contributore voglio inviare una ricetta per la revisione così appare nel catalogo dopo l'approvazione.

## 7. Requisiti Funzionali
- RF1: Registrazione/accesso con email + OAuth (Google, Apple).
- RF2: Creazione/lettura/modifica/eliminazione ricette con cronologia delle versioni.
- RF3: Analisi delle righe degli ingredienti in quantità, unità, ingrediente, note.
- RF4: Conversione delle unità tra metrico e imperiale.
- RF5: Ricerca full-text e filtraggio per tag.
- RF6: Valutazione (1–5) e commenti con strumenti di moderazione.
- RF7: Condivisione ricetta tramite URL e piattaforme social.
- RF8: Esportazione ricetta come PDF stampabile.

## 8. Requisiti Non Funzionali
- RNF1: Tempo di risposta < 300ms per le query di ricerca.
- RNF2: Lettura offline per le ricette salvate entro 24 ore dal salvataggio.
- RNF3: Disponibilità 99,9% mensile.
- RNF4: Backup dei dati giornaliero, conservazione 30 giorni.
- RNF5: Scalabile fino a 1 milione di utenti.

## 9. Modello dei Dati (alto livello)
- Utente { id, nome, email, providerAutenticazione, preferenze, createdAt }
- Ricetta { id, titolo, autoreId, ingredienti[], passaggi[], foto[], tag[], porzioni, tempoPreparazione, difficoltà, stimaABV, stato, createdAt }
- Ingrediente { nome, quantità, unità, preparazione }
- Collezione { id, proprietarioId, titolo, idRicette[], visibilità }
- Valutazione { utenteId, ricettaId, punteggio }
- Commento { utenteId, ricettaId, testo, createdAt, moderato }

## 10. Endpoint API (esempi)
- GET /ricette?query=&filtri=
- GET /ricette/{id}
- POST /ricette
- PUT /ricette/{id}
- POST /auth/login
- POST /utenti/{id}/collezioni

## 11. UX e Accessibilità
- UI responsive mobile-first.
- Sequenza chiara dei passaggi della ricetta e timer.
- Conformità WCAG 2.1 AA: navigazione da tastiera, HTML semantico, testo alternativo per le immagini, contrasto dei colori.

## 12. Sicurezza e Privacy
- Cifratura dei dati sensibili a riposo e in transito (TLS).
- Limitazione della velocità sugli endpoint pubblici.
- Age-gating opzionale (visualizzazione avviso).
- Conformità al GDPR: esportazione ed eliminazione dei dati utente.

## 13. Test e Criteri di Accettazione
- Test unitari per la logica di analisi e dosaggio (copertura ≥ 90%).
- Test di integrazione per il flusso di ricerca e invio.
- Test UX manuale sui principali dispositivi e browser.
- Accettazione: i flussi principali (ricerca, visualizzazione, salvataggio, invio) superano i test end-to-end.

## 14. Metriche e Analisi
- Monitorare DAU/MAU, conversione (registrazione dopo visualizzazione), salvataggi ricette, tasso di condivisione, valutazione media.
- Test A/B degli algoritmi di raccomandazione della homepage.

## 15. Roadmap / Milestone
- M1 (4 settimane): Modello dati principale, CRUD ricette, UI di base.
- M2 (8 settimane): Ricerca, filtri, dosaggio, conversione unità.
- M3 (12 settimane): Autenticazione, invio ricette, moderazione.
- M4 (16 settimane): Supporto offline, esportazione PDF, analisi.

## 16. Domande Aperte
- Modello di moderazione: community o centralizzato?
- Livello di normalizzazione degli ingredienti richiesto per la qualità delle raccomandazioni.
