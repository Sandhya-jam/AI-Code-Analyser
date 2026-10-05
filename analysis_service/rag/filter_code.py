from pathlib import Path
import shutil

SOURCE = Path("knowledge/dsa/raw/code_examples/Python")
DEST = Path("knowledge/dsa/processed/code_examples")

CATEGORIES = {
    "sorts",
    "searches",
    "data_structures",
    "divide_and_conquer",
    "dynamic_programming",
    "graphs",
    "greedy_methods",
    "backtracking",
    "strings",
}

DEST.mkdir(parents=True, exist_ok=True)
count = 0

for category in CATEGORIES:
    source_dir = SOURCE / category
    if not source_dir.exists():
        print(f"Skipping missing category: {category}")
        continue
    
    destination_dir = DEST / category
    destination_dir.mkdir(parents=True, exist_ok=True)

    for file in source_dir.rglob("*.py"):
        # Ignore tests
        if "test" in file.name.lower():
            continue

        shutil.copy2(
            file,
            destination_dir / file.name
        )

        count += 1

print(f"\nCopied {count} Python algorithm files.")