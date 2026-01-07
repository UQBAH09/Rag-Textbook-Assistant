import re
from sentence_transformers import SentenceTransformer

# Load embedding model once
_model = SentenceTransformer("all-MiniLM-L6-v2")


def split_sentences(text):
    """Split text conservatively into sentences."""
    return re.split(r'(?<!\d)(?<=[.!?])\s+', text)


def create_chunks(text, min_size=300, max_size=800):
    """Group sentences into size-bounded chunks."""
    sentences = split_sentences(text)

    chunks = []
    current = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        if current_len + sentence_len > max_size and current_len >= min_size:
            chunks.append(" ".join(current))
            current = []
            current_len = 0

        current.append(sentence)
        current_len += sentence_len

    if current:
        chunks.append(" ".join(current))

    return chunks


def chunk_book(book):
    """Convert structured book into flat list of chunks."""
    all_chunks = []

    for chapter_key, chapter_data in book.items():
        chapter_num = int(chapter_key.split()[-1])

        for section_id, section_text in chapter_data["sections"].items():
            chunks = create_chunks(section_text)

            for chunk_id, chunk_text in enumerate(chunks):
                all_chunks.append({
                    "chapter": chapter_num,
                    "section": section_id,
                    "chunk_id": chunk_id,
                    "text": chunk_text
                })

    return all_chunks


def embed_text(text):
    """Embed a single string."""
    return _model.encode(text).tolist()


def embed_chunks(chunks):
    """Embed chunks in-place."""
    for chunk in chunks:
        chunk["embedding"] = embed_text(chunk["text"])
    return chunks


def build_embedded_chunks(book):
    """Full pipeline: structured book → embedded chunks."""
    chunks = chunk_book(book)
    return embed_chunks(chunks)
