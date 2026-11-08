import re
from collections import Counter


def split_chunks(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
    return chunks


def retrieve_relevant_chunks(text: str, question: str, limit: int = 4) -> list[str]:
    chunks = split_chunks(text)
    terms = [t for t in re.findall(r"[\wÀ-ÿ]+", question.lower()) if len(t) > 2]
    if not chunks:
        return []
    if not terms:
        return chunks[:limit]
    scored = []
    for index, chunk in enumerate(chunks):
        words = re.findall(r"[\wÀ-ÿ]+", chunk.lower())
        counts = Counter(words)
        score = sum(counts[t] for t in terms)
        scored.append((score, -index, chunk))
    scored.sort(reverse=True)
    selected = [item[2] for item in scored[:limit] if item[0] > 0]
    return selected or chunks[:min(limit, len(chunks))]
