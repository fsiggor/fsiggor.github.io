"""Load crawler markdown docs, create embeddings, and store in ChromaDB."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

from openai import OpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CHROMA_DIR = Path(__file__).resolve().parents[1] / "chroma_db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents(data_dir: Path) -> list:
    loader = DirectoryLoader(
        str(data_dir),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def split_documents(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    return splitter.split_documents(docs)


def create_vectorstore(chunks: list, persist_dir: Path, model: str) -> Chroma:
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    embeddings = OpenAIEmbeddings(model=model, client=client.embeddings)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="crawler_docs",
    )
    return vectorstore


def ingest(data_dir: Path = DATA_DIR, persist_dir: Path = CHROMA_DIR, model: str = "text-embedding-3-small") -> int:
    docs = load_documents(data_dir)
    if not docs:
        print("No documents found.")
        return 0

    print(f"Loaded {len(docs)} documents")

    chunks = split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    create_vectorstore(chunks, persist_dir, model)
    print(f"Stored embeddings in {persist_dir}")

    return len(chunks)


def main():
    parser = argparse.ArgumentParser(description="Ingest crawler docs into ChromaDB")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR, help="Path to markdown files")
    parser.add_argument("--chroma-dir", type=Path, default=CHROMA_DIR, help="Path to ChromaDB storage")
    parser.add_argument("--model", default="text-embedding-3-small", help="OpenAI embedding model")
    args = parser.parse_args()

    ingest(args.data_dir, args.chroma_dir, args.model)


if __name__ == "__main__":
    main()
