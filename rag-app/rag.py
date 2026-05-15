"""
RAG (Retrieval-Augmented Generation) Logic
-------------------------------------------
This file handles everything behind the scenes:
1. Loading a document (PDF or TXT)
2. Splitting it into small chunks
3. Turning chunks into embeddings (numbers that represent meaning)
4. Storing embeddings in ChromaDB (a vector database)
5. Answering questions by finding relevant chunks and asking the LLM
"""

import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

CHROMA_DIR = "./chroma_db"


def build_index(file_path: str):
    """
    Load a document, split it into chunks, embed them, and store in ChromaDB.
    Clears any previous index first so stale data never bleeds into new queries.
    Returns the QA chain (caller should store it in st.session_state).
    """
    # --- Clear old ChromaDB data before indexing a new file ---
    # Without this, uploading File B would also return results from File A.
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # --- Step 1: Load the document ---
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # --- Step 2: Split into chunks ---
    # chunk_size=500 chars each, chunk_overlap=50 keeps a little context between chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # --- Step 3: Embed and store in ChromaDB ---
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # --- Step 4: Build and return the QA chain ---
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain  # caller stores this in st.session_state


def ask(qa_chain, question: str) -> str:
    """
    Ask a question using the provided QA chain. Returns the answer string.
    """
    result = qa_chain.invoke({"query": question})
    return result["result"]
