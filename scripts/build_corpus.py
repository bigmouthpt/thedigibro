from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.scraper import UrlScraper


def chunk_text(text: str, chunk_size: int = 1200) -> list[str]:
    clean = " ".join(text.split())
    return [clean[i : i + chunk_size] for i in range(0, len(clean), chunk_size)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build corpus from newsletter URLs")
    parser.add_argument("--input", required=True, help="File txt con una URL per riga")
    parser.add_argument("--output", default="data/corpus.json", help="Path output JSON")
    args = parser.parse_args()

    urls = [u.strip() for u in Path(args.input).read_text(encoding="utf-8").splitlines() if u.strip()]
    scraper = UrlScraper()
    docs = scraper.scrape(urls)

    corpus = []
    for doc in docs:
        for chunk in chunk_text(doc.text):
            corpus.append({"source": doc.url, "title": doc.title, "text": chunk})

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Creati {len(corpus)} chunk in {args.output}")


if __name__ == "__main__":
    main()
