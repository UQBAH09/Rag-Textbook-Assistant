def build_context(chunks):
    """
    Combine retrieved chunks into a readable context block.
    """
    parts = []

    for c in chunks:
        header = f"[Chapter {c['chapter']} – Section {c['section']}]"
        parts.append(f"{header}\n{c['text']}")

    return "\n\n".join(parts)


def build_qa_prompt(query, context):
    """
    Prompt for answering questions using textbook content only.
    """
    return f"""
You are an educational assistant.

Use ONLY the textbook content provided below to answer the question.
If the answer is not present, say:
"Not found in the provided text."

TEXTBOOK CONTENT:
{context}

QUESTION:
{query}

ANSWER:
""".strip()


def build_question_generation_prompt(context, num_questions=5):
    """
    Prompt for generating questions from textbook content.
    """
    return f"""
You are an educational assistant.

Using ONLY the textbook content below, generate {num_questions}
clear and relevant exam-style questions.

TEXTBOOK CONTENT:
{context}

QUESTIONS:
""".strip()
