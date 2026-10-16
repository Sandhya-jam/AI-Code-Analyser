from pathlib import Path
import json
from pypdf import PdfReader

SOURCE = Path("knowledge/dsa/raw/algorithms")
OUTPUT = Path(
    "knowledge/dsa/processed/documents/theory_documents.jsonl"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

documents = []

for pdf_file in sorted(SOURCE.glob("*.pdf")):

    print(f"Processing: {pdf_file.name}")

    try:
        reader = PdfReader(str(pdf_file))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        full_text = "\n".join(pages).strip()

        if not full_text:
            print(f"  WARNING: No text extracted")
            continue

        document = {
            "text": full_text,
            "metadata": {
                "source": "MIT 6.006",
                "language": "general",
                "type": "theory",
                "filename": pdf_file.name,
                "pages": len(reader.pages)
            }
        }

        documents.append(document)

    except Exception as e:
        print(f"  ERROR: {e}")


with open(OUTPUT, "w", encoding="utf-8") as f:

    for document in documents:
        f.write(
            json.dumps(document, ensure_ascii=False)
            + "\n"
        )


print("\n==============================")
print(f"Documents created: {len(documents)}")
print(f"Output: {OUTPUT}")
print("==============================")