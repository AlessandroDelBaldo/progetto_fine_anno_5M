# Documentazione Tecnica — CocktailHub Backend

---

## 1. Introduzione

Il progetto è un'applicazione web per la gestione di un ricettario di cocktail (CocktailHub) sviluppata con Python e Flask. Permette di:
- consultare, creare, modificare e cancellare cocktail;
- gestire ingredienti e categorie (tipi di cocktail);
- cercare cocktail per nome o ingrediente;
- salvare cocktail tra i preferiti;
- lasciare commenti sui cocktail;
- registrarsi, accedere e recuperare la password via email.

L'interfaccia è basata su template HTML Jinja2 con CSS personalizzato. Il backend utilizza SQLite come database e segue il Repository Pattern, organizzato in due Blueprint Flask (`main` e `auth`).

---

## 2. Obiettivi generali

- Permettere a chiunque di consultare l'elenco dei cocktail e cercarli (senza autenticazione).
- Consentire agli utenti registrati di vedere i dettagli, creare, modificare e cancellare cocktail.
- Permettere agli utenti autenticati di salvare preferiti e lasciare commenti.
- Organizzare il codice con Blueprint e Repository Pattern per testabilità e manutenzione.

---

## 3. Funzionalità implementate

### Route — Blueprint `main`

| Metodo | URL | Autenticazione | Descrizione |
|--------|-----|:-:|-------------|
| GET | `/` | No | Home: lista cocktail con ricerca |
| GET | `/search?q=<testo>` | No | Ricerca per nome o ingrediente |
| GET | `/cocktails` | No | Elenco completo cocktail |
| GET | `/cocktails/<id>` | Sì | Dettaglio cocktail con commenti e preferito |
| GET/POST | `/cocktails/create` | Sì | Crea nuovo cocktail |
| GET/POST | `/cocktails/<id>/edit` | Sì | Modifica cocktail |
| POST | `/cocktails/<id>/delete` | Sì | Elimina cocktail |
| POST | `/cocktails/<id>/comment` | Sì | Aggiunge un commento |
| POST | `/cocktails/<id>/comment/<cid>/delete` | Sì | Elimina un commento |
| POST | `/cocktails/<id>/favorite` | Sì | Aggiunge/rimuove dai preferiti |
| GET | `/preferiti` | Sì | Lista cocktail preferiti dell'utente |

### Route — Blueprint `auth`

| Metodo | URL | Descrizione |
|--------|-----|-------------|
| GET/POST | `/auth/login` | Login con email e password |
| GET/POST | `/auth/register` | Registrazione nuovo utente |
| GET | `/auth/logout` | Logout |
| GET/POST | `/auth/forgot-password` | Richiesta reset password via email |
| GET/POST | `/auth/reset-password/<token>` | Reset password con token |

### User stories

- Come visitatore, voglio vedere l'elenco dei cocktail e cercarli per nome o ingrediente.
- Come utente autenticato, voglio vedere i dettagli di un cocktail, i suoi ingredienti e i commenti.
- Come utente autenticato, voglio creare, modificare ed eliminare i miei cocktail.
- Come utente, voglio salvare i cocktail preferiti per ritrovarli facilmente.
- Come utente, voglio lasciare commenti sui cocktail.

---

## 4. Requisiti non funzionali

- Password memorizzate con hashing sicuro (Werkzeug `generate_password_hash`).
- Utilizzo di database relazionale leggero (SQLite).
- Struttura modulare con Blueprint (`main`, `auth`) e repository separati per accesso ai dati.
- Ambiente virtuale Python (`venv`) per isolare le dipendenze.
- Reset password via email con token a scadenza (1 ora), configurabile tramite variabili SMTP.

---

## 5. Schema ER (Entità e Relazioni)

```mermaid
erDiagram
    USERS {
        int id PK
        string email
        string username
        string password_hash
        string reset_token
        real reset_token_expires
    }
    COCKTAIL_TYPES {
        int id PK
        string name
        string description
    }
    COCKTAILS {
        int id PK
        string name
        string country
        string region
        int preparation_time_minutes
        int cocktail_type_id FK
        string instructions
        string image_url
        string api_id
        real abv
    }
    INGREDIENTS {
        int id PK
        string name
        string default_unit
        string image_url
    }
    COCKTAIL_INGREDIENTS {
        int cocktail_id FK
        int ingredient_id FK
        real quantity
        string unit
    }
    FAVORITES {
        int user_id FK
        int cocktail_id FK
    }
    COMMENTS {
        int id PK
        int cocktail_id FK
        int user_id FK
        string content
        string created_at
    }

    COCKTAIL_TYPES ||--o{ COCKTAILS : classifica
    COCKTAILS ||--o{ COCKTAIL_INGREDIENTS : contiene
    INGREDIENTS ||--o{ COCKTAIL_INGREDIENTS : utilizzato_in
    USERS ||--o{ FAVORITES : salva
    COCKTAILS ||--o{ FAVORITES : salvato_da
    USERS ||--o{ COMMENTS : scrive
    COCKTAILS ||--o{ COMMENTS : riceve
```

> Nota: COCKTAIL_INGREDIENTS è un'entità associativa many-to-many tra COCKTAILS e INGREDIENTS, con quantity e unit specifiche per ogni ricetta.

---

## 6. Diagramma UML delle classi (semplificato)

```mermaid
classDiagram
    class auth_Blueprint {
        +login()
        +register()
        +logout()
        +forgot_password()
        +reset_password(token)
        +login_required()
    }
    class main_Blueprint {
        +index()
        +search_page()
        +search_cocktails()
        +cocktail_detail(id)
        +create_cocktail()
        +edit_cocktail(id)
        +delete_cocktail(id)
        +add_comment(id)
        +delete_comment(id, cid)
        +toggle_favorite(id)
        +favorites()
    }
    class CocktailRepository {
        +get_all_cocktails()
        +search_cocktails(term)
        +get_cocktail_by_id(id)
        +create_cocktail(data)
        +update_cocktail(id, data)
        +delete_cocktail(id)
    }
    class UserRepository {
        +get_user_by_email(email)
        +get_user_by_username(username)
        +create_user(email, username, hash)
        +set_reset_token(id, token, exp)
        +get_user_by_reset_token(token)
        +update_password(id, hash)
        +clear_reset_token(id)
    }
    class CommentRepository {
        +get_comments_for_cocktail(id)
        +add_comment(cocktail_id, user_id, content)
        +delete_comment(comment_id, user_id)
    }
    class FavoriteRepository {
        +is_favorite(user_id, cocktail_id)
        +toggle_favorite(user_id, cocktail_id)
        +get_favorite_cocktails(user_id)
    }
    class IngredientRepository {
        +get_all_ingredients()
        +get_ingredient_by_id(id)
        +create_ingredient(name, unit)
        +update_ingredient(id, data)
        +delete_ingredient(id)
    }
    class CocktailTypeRepository {
        +get_all_cocktail_types()
        +get_cocktail_type_by_id(id)
        +create_cocktail_type(name, desc)
    }
    class CocktailIngredientRepository {
        +get_ingredients_for_cocktail(id)
        +add_ingredient_to_cocktail(data)
        +update_cocktail_ingredient(data)
        +delete_cocktail_ingredient(data)
    }

    auth_Blueprint ..> UserRepository
    main_Blueprint ..> CocktailRepository
    main_Blueprint ..> IngredientRepository
    main_Blueprint ..> CocktailTypeRepository
    main_Blueprint ..> CommentRepository
    main_Blueprint ..> FavoriteRepository
    CocktailRepository ..> CocktailIngredientRepository
```

---

## 7. Glossario

- **Cocktail**: ricetta con nome, ingredienti (quantità e unità), istruzioni e metadati (paese, regione, ABV, tempo).
- **Tipo cocktail** (`cocktail_types`): raggruppamento tematico (es. Classico, Tropicale, Senza alcool).
- **Ingrediente**: voce riutilizzabile (es. Vodka, Succo di limone) con unità di misura predefinita.
- **Preferito**: associazione utente-cocktail che permette di ritrovare rapidamente i cocktail salvati.
- **Commento**: testo scritto da un utente autenticato su un cocktail specifico.

---

## 8. Pianificazione del progetto (sintesi)

- Setup ambiente e DB: 2-3 giorni
- Modello dati e repository: 3-4 giorni
- Blueprint `main` e route pubbliche: 2-3 giorni
- Blueprint `auth` (login, registrazione, reset password): 3-4 giorni
- Preferiti e commenti: 2-3 giorni
- Template HTML e CSS: 2-3 giorni
- Test e documentazione: 2-3 giorni

---

## 9. Casi d'uso (sintesi)

**Attori:** Visitatore, Utente autenticato.

Principali casi d'uso:
- Consultare la lista dei cocktail e cercarli per nome o ingrediente (pubblico)
- Consultare il dettaglio di un cocktail con ingredienti e commenti (utente autenticato)
- Creare, modificare ed eliminare cocktail (utente autenticato)
- Salvare/rimuovere un cocktail dai preferiti (utente autenticato)
- Lasciare ed eliminare commenti (utente autenticato)
- Registrarsi, fare login e recuperare la password (pubblico)
