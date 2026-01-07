![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-green)
![RAG](https://img.shields.io/badge/Architecture-RAG-orange)

# AI Textbook Question Generator (RAG)

This project builds a Retrieval-Augmented Generation (RAG) system
that can read a textbook PDF, index it using vector embeddings,
and answer questions or generate exam-style questions from it.

## Features
- PDF ingestion
- Chapter & section parsing
- Sentence chunking
- Vector embeddings (SentenceTransformers)
- FAISS semantic search
- Gemini LLM integration
- Debug mode for retrieved chunks

## Setup

```bash
git clone https://github.com/yourusername/ai-bot-reader.git
cd ai-bot-reader
pip install -r requirements.txt
