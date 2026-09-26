import os
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Optional: Switch to Gemini or OpenAI if available
# from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# --- Configuration Settings ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Core_v6.3.pdf")  # Path to the Bluetooth Spec PDF
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "bluetooth_chroma_db")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
CHUNK_SIZE = 1200       # Larger chunk size for dense technical specs
CHUNK_OVERLAP = 200     # Overlap to prevent splitting critical context


def load_and_chunk_pdf(pdf_path: str):
    """Loads a large PDF and splits it into manageable chunks."""
    print(f"Loading {pdf_path}... (This may take 1-2 minutes for large files)")
    loader = PyPDFLoader(pdf_path)
    
    # Load page by page
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF.")

    # Configure text splitter optimized for technical documentation
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\nSection ", "\n\n", "\n", " ", ""],
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")
    return chunks


def build_or_load_vectorstore(chunks=None):
    """Embeds chunks into ChromaDB in batches to prevent memory overflow."""
    # Free, high-performance local embedding model (runs on CPU/GPU)
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # Change to 'cuda' if GPU available
    )

    # Check if vector database already exists on disk
    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print("Found existing vector database on disk. Loading database...")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY, 
            embedding_function=embeddings
        )
        return vectorstore

    if chunks is None:
        raise ValueError("No existing database found and no chunks provided to build one.")

    print("Building new ChromaDB vector database in batches...")
    
    # Initialize empty Chroma database
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    # Add chunks in batches of 500 to handle high page counts cleanly
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vectorstore.add_documents(documents=batch)
        print(f"Indexed batch {i // batch_size + 1}/{(len(chunks) // batch_size) + 1}")
    
    print("Database indexing complete and saved to disk!")
    return vectorstore


def query_bluetooth_spec(vectorstore, query: str, llm):
    """Retrieves relevant context and generates an answer."""
    # Retrieve top 4 most relevant chunks
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(query)
    
    # Combine retrieved context and capture page metadata
    context = "\n\n---\n\n".join([doc.page_content for doc in docs])
    sources = set([f"Page {doc.metadata.get('page', 'Unknown') + 1}" for doc in docs])

    # System prompt strictly instructing model to rely on context
    template = """
    You are an expert embedded software engineer specializing in the Bluetooth Core Specification.
    Answer the question based ONLY on the following technical context retrieved from the spec.
    If you do not know the answer or if it's not present in the context, state that clearly.

    Retrieved Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    print(f"\nQuerying: '{query}'...")
    response = chain.invoke({"context": context, "question": query})

    print("\n=== Answer ===")
    print(response)
    print(f"\n[Sources Referenced: {', '.join(sources)}]")


if __name__ == "__main__":
    # 1. Setup LLM (Using Google Gemini as an example, replace with your LLM of choice)
    # Ensure GOOGLE_API_KEY is in your .env file, or swap with ChatOpenAI/Ollama
    from langchain_google_genai import ChatGoogleGenerativeAI

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is missing. Add it to your .env file or environment variables.")

    try:
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.1)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to initialize Gemini model '{MODEL_NAME}'. "
            "Use a currently available model such as 'gemini-3.8-flash' or update your GEMINI_MODEL value."
        ) from exc

    # 2. Build or Load Index
    if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
        chunks = load_and_chunk_pdf(PDF_PATH)
        vectorstore = build_or_load_vectorstore(chunks)
    else:
        vectorstore = build_or_load_vectorstore()

    # 3. Test Question
    test_query = "What is the maximum advertising data length in Bluetooth 5.0 and LE Extended Advertising?"
    query_bluetooth_spec(vectorstore, test_query, llm)