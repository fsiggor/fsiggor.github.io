# Embeddings

Semantic embeddings for crawler documents using LangChain + ChromaDB + OpenAI.

## Setup

```bash
cd embeddings
uv sync
```

Requires Python 3.12-3.13 and [uv](https://docs.astral.sh/uv/).

### Configuration

Edit `.env` with your API key. The scripts load it automatically via `python-dotenv`.

**OpenAI (direct):**
```
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=
```

**OpenRouter (alternative):**
```
OPENAI_API_KEY=sk-or-...
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

## Usage

### Ingest documents

Loads all markdown files from `data/`, splits into chunks, and stores embeddings in ChromaDB:

```bash
uv run python src/ingest.py
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--data-dir` | `../data` | Path to crawler markdown files |
| `--chroma-dir` | `./chroma_db` | Path to ChromaDB storage |
| `--model` | `text-embedding-3-small` | OpenAI embedding model |

### Query documents

Search for similar documents by semantic similarity:

```bash
uv run python src/query.py "flag theory offshore banking"
```

| Argument | Default | Description |
|----------|---------|-------------|
| `query` | (required) | Search query |
| `--k` | `5` | Number of results |
| `--chroma-dir` | `./chroma_db` | Path to ChromaDB storage |
| `--model` | `text-embedding-3-small` | OpenAI embedding model |

## Project structure

```
embeddings/
├── src/
│   ├── __init__.py
│   ├── ingest.py     # Load docs, chunk, embed, store in ChromaDB
│   └── query.py      # Semantic search over stored embeddings
├── chroma_db/        # ChromaDB storage (gitignored)
├── .env              # API keys template (gitignored)
├── pyproject.toml
└── README.md
```
