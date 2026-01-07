import pdfplumber
import re


def extract_text_from_pdf(file_path, num_pages=None):
    """
    Extract raw text from a PDF.
    Optionally limit pages for debugging.
    """
    all_text = []

    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages if num_pages is None else pdf.pages[:num_pages]

        for page in pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

    return "\n\n".join(all_text)


def find_sections(chapter_text, chapter_num):
    """
    Split a chapter into its sections (e.g. 4.1, 4.2),
    ensuring sections belong to the correct chapter.
    """
    section_pattern = r"(\d+\.\d+\.?[\s\S]*?)(?=\n\d+\.\d+\.?|\Z)"
    raw_sections = re.findall(section_pattern, chapter_text)

    sections = {}
    chapter_num = int(chapter_num)

    for sec in raw_sections:
        lines = [l.strip() for l in sec.splitlines() if l.strip()]
        if not lines:
            continue

        match = re.match(r"(\d+)\.(\d+)", lines[0])
        if not match:
            continue

        sec_chapter = int(match.group(1))
        sec_id = f"{match.group(1)}.{match.group(2)}"

        # Prevent header/footer noise from creating fake sections
        if sec_chapter == chapter_num:
            sections[sec_id] = sec.strip()

    return sections


def structure_book(text):
    """
    Split the full book text into chapters and sections.
    """
    chapter_pattern = r"(CHAPTER\s+\d+[\s\S]*?)(?=CHAPTER\s+\d+|\Z)"
    raw_chapters = re.findall(chapter_pattern, text, re.IGNORECASE)

    book = {}
    prev_num = None
    prev_title = ""
    prev_content = ""

    for chp in raw_chapters:
        lines = [l.strip() for l in chp.splitlines() if l.strip()]
        if not lines:
            continue

        chapter_num = re.search(r"\d+", lines[0]).group()
        chapter_title = lines[1] if len(lines) > 1 else ""
        content_only = "\n".join(lines[1:])

        # Handle repeated chapter headers from page headers
        if chapter_num == prev_num:
            prev_content += "\n" + content_only
        else:
            if prev_num is not None:
                book[f"Chapter {prev_num}"] = {
                    "title": prev_title,
                    "sections": find_sections(prev_content, prev_num)
                }

            prev_num = chapter_num
            prev_title = chapter_title
            prev_content = content_only

    # Save final chapter
    if prev_num is not None:
        book[f"Chapter {prev_num}"] = {
            "title": prev_title,
            "sections": find_sections(prev_content, prev_num)
        }

    return book


def ingest_book(file_path, num_pages=None):
    """
    Full ingestion pipeline: PDF → structured chapters & sections.
    """
    text = extract_text_from_pdf(file_path, num_pages)
    return structure_book(text)
