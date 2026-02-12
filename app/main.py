from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.rag import NewsletterBrain

load_dotenv()

app = FastAPI(title="Newsletter Tone Bot")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

brain: NewsletterBrain | None = None


@app.on_event("startup")
def startup_event() -> None:
    global brain
    corpus = Path(os.getenv("CORPUS_PATH", "data/corpus.json"))
    if corpus.exists() and os.getenv("OPENAI_API_KEY"):
        brain = NewsletterBrain(corpus_path=corpus)
        brain.load()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    payload = await request.json()
    message = payload.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Messaggio vuoto."}, status_code=400)

    if brain is None:
        return JSONResponse(
            {
                "answer": (
                    "Bot non inizializzato: configura OPENAI_API_KEY e genera data/corpus.json "
                    "con gli articoli della tua newsletter."
                )
            }
        )

    answer = brain.answer(message)
    return JSONResponse({"answer": answer})
