from pathlib import Path
import ast
import json

source_file = Path(
    "knowledge/dsa/processed/documents/code_documents.jsonl"
)

total = 0
with_imports = 0
with_module_statements = 0

with source_file.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        document = json.loads(line)
        total += 1

        try:
            tree = ast.parse(document["text"])
        except SyntaxError:
            continue

        if any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            for node in tree.body
        ):
            with_imports += 1

        if any(
            not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                    ast.Import,
                    ast.ImportFrom,
                ),
            )
            for node in tree.body
        ):
            with_module_statements += 1

print("Source files checked:", total)
print("Files containing top-level imports:", with_imports)
print("Files containing other top-level statements:", with_module_statements)