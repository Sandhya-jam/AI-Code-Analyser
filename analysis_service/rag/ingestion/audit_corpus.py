
from pathlib import Path
import ast
import json
from collections import Counter

RAG_DIR = Path(__file__).resolve().parent.parent
BASE = RAG_DIR / "knowledge" / "dsa" / "processed"

SOURCE_FILE = BASE / "documents" / "code_documents.jsonl"
CHUNK_FILE = BASE / "chunks" / "code" / "code_chunks.jsonl"

source_documents = {}

with SOURCE_FILE.open("r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            doc = json.loads(line)
            source_documents[doc["metadata"]["path"]] = doc

issues = Counter()
examples = []

with CHUNK_FILE.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        chunk = json.loads(line)
        meta = chunk["metadata"]
        path = meta.get("path")
        filename = meta.get("filename")
        chunk_name = meta.get("chunk_name")

        source = source_documents.get(path)

        if source is None:
            issues["missing_source_path"] += 1
            examples.append((chunk.get("chunk_id"), "Missing source", path))
            continue

        if Path(path).name != filename:
            issues["filename_path_mismatch"] += 1
            examples.append((chunk.get("chunk_id"), "Filename mismatch", path))

        try:
            tree = ast.parse(source["text"])
            names = {
                node.name
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
                )
            }
        except SyntaxError as e:
            issues["source_syntax_error"] += 1
            examples.append((
                path,
                f"Syntax error at line {e.lineno}: {e.msg}"
            ))
            continue

        if chunk_name and chunk_name not in names:
            issues["chunk_name_not_in_source"] += 1
            examples.append((
                chunk.get("chunk_id"),
                f"Name {chunk_name!r} not found in source",
                path,
            ))

        if chunk.get("text", "").strip() not in source["text"]:
            issues["chunk_text_not_exact_source_segment"] += 1

print("Source documents:", len(source_documents))
print("Issues:")
for name, count in issues.items():
    print(f"  {name}: {count}")

print("\nFirst 20 examples:")
for example in examples[:20]:
    print(example)