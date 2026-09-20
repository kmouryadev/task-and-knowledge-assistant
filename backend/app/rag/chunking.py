import re

from pydantic import BaseModel

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


class Chunk(BaseModel):
    content: str
    section: str | None
    chunk_index: int


def _split_by_heading(text: str) -> list[tuple[str | None, str]]:
    matches = list(_HEADING_RE.finditer(text))
    if not matches:
        return [(None, text)]

    sections: list[tuple[str | None, str]] = []
    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((heading, body))
    return sections or [(None, text)]


def _chunk_body(body: str, chunk_size: int, overlap: int) -> list[str]:
    if len(body) <= chunk_size:
        return [body]

    chunks = []
    start = 0
    step = chunk_size - overlap
    while start < len(body):
        end = min(start + chunk_size, len(body))
        chunks.append(body[start:end])
        if end == len(body):
            break
        start += step
    return chunks


def chunk_markdown(
    text: str,
    source: str,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[Chunk]:
    text = text.strip()
    if not text:
        return []

    chunks: list[Chunk] = []
    for section, body in _split_by_heading(text):
        for piece in _chunk_body(body, chunk_size, overlap):
            if piece.strip():
                chunks.append(
                    Chunk(content=piece.strip(), section=section, chunk_index=len(chunks))
                )
    return chunks
