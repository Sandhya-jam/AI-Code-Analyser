from pathlib import Path
import json
import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

INGESTION_DIR = Path(__file__).resolve().parent
RAG_DIR = INGESTION_DIR.parent

CHUNKS_DIR = (
    RAG_DIR / "knowledge" / "dsa" / "processed" / "chunks"
)
DB_DIR = RAG_DIR / "chroma"
INPUT_FILES = [
    CHUNKS_DIR / "code" / "code_chunks.jsonl",
    CHUNKS_DIR / "theory" / "theory_chunks.jsonl",
    CHUNKS_DIR / "complexity" / "complexity_chunks.jsonl",
    CHUNKS_DIR / "algorithm_complexity"/ "algorithm_complexity_chunks.jsonl",
]

COLLECTION_NAME = "dsa_knowledge"
BATCH_SIZE = 100

# EMBEDDING MODEL

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

#INITIALIZE CHROMADB

client = chromadb.PersistentClient(path=str(DB_DIR))


COLLECTION_NAME = "dsa_knowledge"

# Delete the previous collection to prevent stale chunks.
existing_collections = [
    item.name for item in client.list_collections()
]

if COLLECTION_NAME in existing_collections:
    client.delete_collection(name=COLLECTION_NAME)
    print(f"Deleted old collection: {COLLECTION_NAME}")

# Create a fresh collection using the same embedding model.
collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

# LOAD CHUNKS

def load_chunks():
    documents = []
    metadatas = []
    ids = []

    seen_ids = set()

    for file_path in INPUT_FILES:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Chunk file not found: {file_path}\n"
                "Run the document chunking script first."
            )
        print(f"Loading: {file_path.name}")

        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                chunk = json.loads(line)
                chunk_id = chunk["chunk_id"]
                text = chunk["text"].strip()

                if not text:
                    continue

                if chunk_id in seen_ids:
                    raise ValueError(
                        f"Duplicate chunk ID {chunk_id} "
                        f"found in {file_path.name}:{line_number}"
                    )

                seen_ids.add(chunk_id)

                metadata = dict(chunk["metadata"])
                metadata["chunk_id"] = chunk_id

                # Chroma metadata values must be supported scalar types.
                # Keep the code context separately for later retrieval.
                context = chunk.get("context", "")
                if context:
                    metadata["context"] = context

                documents.append(text)
                metadatas.append(metadata)
                ids.append(chunk_id)

    return documents, metadatas, ids

# INGEST IN BATCHES
def ingest():
    documents, metadatas, ids = load_chunks()

    print(f"\nTotal chunks loaded: {len(ids)}")

    for start in range(0, len(ids), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(ids))

        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )

        print(f"Upserted {end}/{len(ids)} chunks")

    print("\n========== INGESTION COMPLETE ==========")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Database: {DB_DIR}")
    print(f"Chunks loaded: {len(ids)}")
    print(f"Chunks in collection: {collection.count()}")

if __name__ == "__main__":
    ingest()
