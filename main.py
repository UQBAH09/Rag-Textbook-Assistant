from Core.book import Book

def main():
    print("=== Textbook RAG ===\n")

    pdf_path = input("Enter path to textbook PDF: ").strip()
    book_id = input("Enter book name: ").strip()

    book = Book(book_id, pdf_path)

    print("\nBook indexed successfully.")
    print("Ask questions (type -1 to exit).\n")

    while True:
        query = input("Question: ").strip()

        if query == "-1":
            break

        answer = book.ask(query)
        print("\nAnswer:")
        print(answer)
        print("-" * 60)


if __name__ == "__main__":
    main()
