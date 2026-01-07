import re
import numpy as np


def extract_section(query):
    match = re.search(r"\b\d+\.\d+\b", query)
    return match.group() if match else None


def extract_chapter(query):
    match = re.search(r"chapter\s+(\d+)", query, re.IGNORECASE)
    return int(match.group(1)) if match else None


def semantic_search(query_embedding, index, chunks, k=5):
    query_vec = np.array([query_embedding], dtype="float32")
    _, indices = index.search(query_vec, k)

    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]


def retrieve_chunks(query, query_embedding, index, chunks, k=5):
    """
    Decide how to retrieve chunks for a query.
    """

    section = extract_section(query)
    chapter = extract_chapter(query)

    # 1. Section-based retrieval
    if section:
        filtered = [c for c in chunks if c["section"] == section]
        if filtered:
            return filtered

    # 2. Chapter-based retrieval
    if chapter is not None:
        filtered = [c for c in chunks if c["chapter"] == chapter]
        if filtered:
            return filtered

    # 3. Semantic fallback
    return semantic_search(query_embedding, index, chunks, k)
