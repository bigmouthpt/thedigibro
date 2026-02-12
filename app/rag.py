from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from openai import OpenAI


@dataclass
class Chunk:
    source: str
    title: str
    text: str


class NewsletterBrain:
    """Indicizza newsletter e reference link per replicare tono di voce."""

    def __init__(self, corpus_path: Path, embedding_model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = embedding_model
        self.corpus_path = corpus_path
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None

    def load(self) -> None:
        raw = json.loads(self.corpus_path.read_text(encoding="utf-8"))
        self.chunks = [Chunk(**item) for item in raw]
        vectors = [self._embed(c.text) for c in self.chunks]
        self.embeddings = np.array(vectors)

    def answer(self, user_message: str, model: str = "gpt-4o-mini") -> str:
        if self.embeddings is None:
            raise RuntimeError("Corpus non caricato. Esegui prima load().")

        query = np.array(self._embed(user_message))
        scores = self.embeddings @ query
        top_idx = np.argsort(scores)[-4:][::-1]
        context = "\n\n".join(
            f"[{self.chunks[i].title} - {self.chunks[i].source}]\n{self.chunks[i].text[:1500]}"
            for i in top_idx
        )

        system_prompt = (
            "Sei il gemello editoriale dell'autore della newsletter. "
            "Rispetta 1:1 il tono (ritmo, lessico, ironia, strutture) osservato nei testi di riferimento, "
            "ma non inventare fatti. Se mancano dati, dichiaralo chiaramente."
        )

        completion = self.client.chat.completions.create(
            model=model,
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Contesto editoriale:\n{context}\n\n"
                        f"Domanda utente:\n{user_message}\n\n"
                        "Rispondi in italiano."
                    ),
                },
            ],
        )
        return completion.choices[0].message.content or "Nessuna risposta generata."

    def _embed(self, text: str) -> list[float]:
        result = self.client.embeddings.create(model=self.embedding_model, input=text[:8000])
        return result.data[0].embedding
