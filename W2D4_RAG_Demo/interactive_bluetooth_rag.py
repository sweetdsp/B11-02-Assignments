import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from bluetooth_rag import (
    MODEL_NAME,
    PDF_PATH,
    PERSIST_DIRECTORY,
    build_or_load_vectorstore,
    load_and_chunk_pdf,
    query_bluetooth_spec,
)


def main():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is missing. Add it to your .env file or environment variables.")

    model_name = os.getenv("GEMINI_MODEL", MODEL_NAME)
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)

    if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
        print("Creating the RAG vector database from the Bluetooth PDF...")
        chunks = load_and_chunk_pdf(PDF_PATH)
        vectorstore = build_or_load_vectorstore(chunks)
    else:
        print("Loading existing Bluetooth RAG database...")
        vectorstore = build_or_load_vectorstore()

    print("\nBluetooth RAG Assistant is ready.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask your Bluetooth question: ").strip()

        if not question:
            print("Please enter a valid question.\n")
            continue

        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        query_bluetooth_spec(vectorstore, question, llm)
        print("\n----------------------------------------\n")


if __name__ == "__main__":
    main()
