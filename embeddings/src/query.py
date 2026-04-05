"""Query the ChromaDB vectorstore for similar documents."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

from openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parents[1] / "chroma_db"


def load_vectorstore(persist_dir: Path = CHROMA_DIR, model: str = "text-embedding-3-small") -> Chroma:
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    embeddings = OpenAIEmbeddings(model=model, client=client.embeddings)
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name="crawler_docs",
    )


def search(query: str, k: int = 5, persist_dir: Path = CHROMA_DIR, model: str = "text-embedding-3-small") -> list:
    vectorstore = load_vectorstore(persist_dir, model)
    return vectorstore.similarity_search_with_score(query, k=k)


def main():
    parser = argparse.ArgumentParser(description="Query crawler embeddings")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--k", type=int, default=5, help="Number of results")
    parser.add_argument("--chroma-dir", type=Path, default=CHROMA_DIR, help="Path to ChromaDB storage")
    parser.add_argument("--model", default="text-embedding-3-small", help="OpenAI embedding model")
    args = parser.parse_args()

    results = search(args.query, args.k, args.chroma_dir, args.model)

    for doc, score in results:
        if score < 0.95:
            continue

        source = doc.metadata.get("source", "unknown")
        print(f"\n#(score: {score:.4f})######################################################################################")
        print(f"\n--- {source} ---")
        print(f"\n################################################################################################")
        # print(doc.page_content[:300])


if __name__ == "__main__":
    main()
