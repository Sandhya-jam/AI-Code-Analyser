from pathlib import Path
import json

SOURCE = Path("knowledge/dsa/processed/code_examples")
OUTPUT = Path("knowledge/dsa/processed/documents/code_documents.jsonl")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

documents = []

for category_dir in SOURCE.iterdir():

    if not category_dir.is_dir():
        continue

    category = category_dir.name

    for file in category_dir.rglob("*.py"):

        # Ignore test files
        if "test" in file.name.lower():
            continue

        try:
            code = file.read_text(encoding="utf-8")

            # Ignore empty/tiny files
            if len(code.strip()) < 50:
                continue

            document = {
                "text": code,
                "metadata": {
                    "source": "TheAlgorithms/Python",
                    "category": category,
                    "language": "python",
                    "type": "code",
                    "filename": file.name,
                    "path": str(file)
                }
            }

            documents.append(document)

        except Exception as e:
            print(f"Could not process {file}: {e}")


with open(OUTPUT, "w", encoding="utf-8") as f:

    for document in documents:
        f.write(json.dumps(document, ensure_ascii=False) + "\n")


print(f"Documents created: {len(documents)}")
print(f"Output: {OUTPUT}")