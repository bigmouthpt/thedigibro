# Newsletter Tone Bot

Mini web app FastAPI che crea un chatbot capace di imitare il tono di voce della tua newsletter usando i numeri passati + link di reference.

## 1) Setup

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

## 3) Avvio app

```bash
uvicorn app.main:app --reload
```

Apri `http://127.0.0.1:8000`.

## Come funziona

1. `build_corpus.py` scarica e pulisce i contenuti.
2. I testi sono divisi in chunk in `data/corpus.json`.
3. All'avvio, `NewsletterBrain` genera embedding dei chunk.
4. A ogni domanda, seleziona i chunk più rilevanti e invia contesto + richiesta al modello chat.

## Prossimi step consigliati

- Sostituire lo scraping base con una pipeline robusta (RSS + parser dedicato per la tua piattaforma newsletter).
- Salvare embedding su un vector DB (Qdrant/pgvector/Pinecone) per scalare meglio.
- Aggiungere prompt-eval automatiche per verificare aderenza al tone of voice.
