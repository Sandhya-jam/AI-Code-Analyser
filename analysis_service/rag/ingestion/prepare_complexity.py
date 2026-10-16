from pathlib import Path
import json

SOURCE = Path("knowledge/dsa/raw/python/time_complexity.txt")
OUTPUT = Path(
    "knowledge/dsa/processed/documents/python_complexity.jsonl"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

text = SOURCE.read_text(encoding="utf-8").strip()

document = {
    "text": text,
    "metadata": {
        "source": "Python Time Complexity Reference",
        "language": "python",
        "type": "complexity",
        "topic": "python_operations"
    }
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(json.dumps(document, ensure_ascii=False) + "\n")

print("Complexity document created!")
print(f"Output: {OUTPUT}")