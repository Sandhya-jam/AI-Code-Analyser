from pathlib import Path
import json

BASE = Path("knowledge/dsa/processed/chunks")

FILES = [
    BASE / "code/code_chunks.jsonl",
    BASE / "theory/theory_chunks.jsonl",
    BASE / "complexity/complexity_chunks.jsonl",
]

for path in FILES:
    print(f"\n{'=' * 60}")
    print(f"FILE: {path}")

    if not path.exists():
        print("File not found!")
        continue

    with path.open("r", encoding="utf-8") as f:
        documents = [json.loads(line) for line in f if line.strip()]

    print("Chunk count:", len(documents))

    for doc in documents[:2]:
        print("\n--- CHUNK ---")
        print("ID:", doc.get("chunk_id"))
        print("Metadata:", doc.get("metadata"))
        print("Context preview:")
        print(doc.get("context", "")[:400])
        print("Text preview:")
        print(doc.get("text", "")[:700])