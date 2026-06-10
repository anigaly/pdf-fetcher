from pdf_fetcher.rag import PDFRAG


def main():
    # Initialize the RAG engine (connects to the existing Qdrant database)
    print("--- Connecting to RAG system... ---")
    rag = PDFRAG()

    print("\nSystem is ready! You can now query your 3 indexed PDF files.")
    print("Type 'exit' to quit the program.")

    # Start an infinite loop for continuous questioning
    while True:
        question = input("\nType your question here: ")

        # Check if the user wants to exit
        if question.lower().strip() == 'exit':
            print("Exiting test script. Goodbye!")
            break

        # Skip empty inputs
        if not question.strip():
            continue

        print("AI is searching the vector database and generating answer...")

        try:
            # Execute the RAG query
            result = rag.ask(question)

            print("\n================== ANSWER ==================")
            print(result["answer"])
            print("============================================")

            # Print references and metadata
            print("\nSources:")
            for source in result["sources"]:
                print(
                    f"- {source['file']} | "
                    f"page {source['page']} | "
                    f"score={source['score']:.3f}"
                )

            print(f"\nScreenshot generated at: {result['screenshot']}")

        except Exception as e:
            print(f"An error occurred while processing the question: {e}")


if __name__ == "__main__":
    main()
