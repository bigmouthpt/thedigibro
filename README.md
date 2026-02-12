# Newsletter Tone Bot

Mini web app FastAPI che crea un chatbot capace di imitare il tono di voce della tua newsletter usando i numeri passati + link di reference.

## 1) Setup locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Aggiungi `OPENAI_API_KEY` in `.env`.

## 2) Costruisci il corpus

Crea `urls.txt` con un URL per riga (newsletter passate e link reference), poi:

```bash
python scripts/build_corpus.py --input urls.txt --output data/corpus.json
```

## 3) Avvio app in locale

```bash
uvicorn app.main:app --reload
```

Apri `http://127.0.0.1:8000`.

---

## Pubblicazione beta su un web server (Render)

Questa repo è pronta per deploy con `render.yaml` + `Dockerfile`.

1. Fai push della repo su GitHub.
2. Vai su Render → **New +** → **Blueprint**.
3. Collega la repo e conferma il file `render.yaml`.
4. Imposta la variabile ambiente `OPENAI_API_KEY`.
5. (Opzionale) imposta `CORPUS_PATH` se diverso da `data/corpus.json`.
6. Deploy.

Al termine avrai una URL pubblica tipo `https://newsletter-tone-bot-beta.onrender.com`.

### Endpoint utili
- `GET /` UI chat
- `POST /chat` endpoint chatbot
- `GET /healthz` health check (`initialized=true/false`)

## Come funziona

1. `build_corpus.py` scarica e pulisce i contenuti.
2. I testi sono divisi in chunk in `data/corpus.json`.
3. All'avvio, `NewsletterBrain` genera embedding dei chunk.
4. A ogni domanda, seleziona i chunk più rilevanti e invia contesto + richiesta al modello chat.

## Prossimi step consigliati

- Sostituire lo scraping base con una pipeline robusta (RSS + parser dedicato per la tua piattaforma newsletter).
- Salvare embedding su un vector DB (Qdrant/pgvector/Pinecone) per scalare meglio.
- Aggiungere prompt-eval automatiche per verificare aderenza al tone of voice.
