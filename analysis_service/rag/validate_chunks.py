
from pathlib import Path
import json

files = [
    Path("knowledge/dsa/processed/chunks/code/code_chunks.jsonl"),
    Path("knowledge/dsa/processed/chunks/theory/theory_chunks.jsonl"),
    Path("knowledge/dsa/processed/chunks/complexity/complexity_chunks.jsonl"),
]

for path in files:
    docs = [
        json.loads(line)
        for line in path.open("r", encoding="utf-8")
        if line.strip()
    ]

    print(f"\n{path.name}: {len(docs)} chunks")

    if "code_chunks" in path.name:
        with_context = sum(bool(d.get("context")) for d in docs)
        print("Chunks with context:", with_context)
        print("First chunk context:", repr(docs[0].get("context", "")[:250]))

    elif "theory_chunks" in path.name:
        for d in docs[:3]:
            print(d["chunk_id"], "tokens:", len(d["text"].split()))
            print("Start:", repr(d["text"][:100]))
            print("End:", repr(d["text"][-100:]))

    else:
        for d in docs:
            print(d["metadata"].get("topic"), ":", repr(d["text"][:70]))
