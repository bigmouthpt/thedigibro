from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests
from bs4 import BeautifulSoup


@dataclass
class ScrapedDocument:
    url: str
    title: str
    text: str


class UrlScraper:
    """Scarica e pulisce il contenuto testuale da pagine web."""

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout

    def scrape(self, urls: Iterable[str]) -> list[ScrapedDocument]:
        docs: list[ScrapedDocument] = []
        for url in urls:
            html = requests.get(url, timeout=self.timeout).text
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup(["script", "style", "noscript"]):
                tag.extract()

            title = (soup.title.string or "Senza titolo").strip() if soup.title else "Senza titolo"
            lines = [line.strip() for line in soup.get_text("\n").splitlines()]
            text = "\n".join(line for line in lines if line)

            docs.append(ScrapedDocument(url=url, title=title, text=text))
        return docs
