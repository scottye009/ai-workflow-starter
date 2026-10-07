from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Chunk:
    source: str
    text: str


def chunk_text(text: str, *, source: str, size: int = 1200, overlap: int = 150) -> list[Chunk]:
    chunks: list[Chunk] = []
    start = 0

    while start < len(text):
        end = min(len(text), start + size)
        piece = text[start:end].strip()
        if piece:
            chunks.append(Chunk(source=source, text=piece))
        if end == len(text):
            break
        start = end - overlap

    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        if not chunks:
            raise ValueError("At least one chunk is required.")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks])

    def search(self, query: str, *, k: int = 4) -> list[tuple[Chunk, float]]:
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        order = scores.argsort()[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in order]


def build_grounded_prompt(query: str, hits: list[tuple[Chunk, float]]) -> str:
    context = "\n\n".join(
        f"[SOURCE {i + 1}: {chunk.source}]\n{chunk.text}"
        for i, (chunk, _) in enumerate(hits)
    )

    return f"""Answer the question using only the supplied evidence.

If the evidence is insufficient, say so explicitly.
Do not invent facts.
Cite supporting sources as [SOURCE N].

QUESTION:
{query}

EVIDENCE:
{context}
"""


def load_txt_folder(path: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    for file in sorted(Path(path).glob("*.txt")):
        chunks.extend(chunk_text(file.read_text(encoding="utf-8"), source=file.name))
    return chunks


if __name__ == "__main__":
    docs = [
        Chunk("policy_a.txt", "Claims must be submitted within 90 days of service."),
        Chunk("policy_b.txt", "Prior authorization is required for the listed services."),
    ]
    retriever = Retriever(docs)
    hits = retriever.search("What is the timely filing limit?")
    print(build_grounded_prompt("What is the timely filing limit?", hits))
