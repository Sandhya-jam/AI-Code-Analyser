from pathlib import Path
import json
import ast
import re
import tiktoken

# CONFIGURATION
BASE=Path("knowledge/dsa/processed")
CODE_INPUT=BASE/"documents/code_documents.jsonl"
THEORY_INPUT = BASE / "documents/theory_documents.jsonl"
COMPLEXITY_INPUT = BASE / "documents/python_complexity.jsonl"

OUTPUT_DIR = BASE / "chunks"

CODE_OUTPUT = OUTPUT_DIR /"code/code_chunks.jsonl"
THEORY_OUTPUT = OUTPUT_DIR /"theory/theory_chunks.jsonl"
COMPLEXITY_OUTPUT = OUTPUT_DIR /"complexity/complexity_chunks.jsonl"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(CODE_OUTPUT.parent).mkdir(parents=True, exist_ok=True)
(THEORY_OUTPUT.parent).mkdir(parents=True, exist_ok=True)
(COMPLEXITY_OUTPUT.parent).mkdir(parents=True, exist_ok=True)

#TOKENIZER
encoding=tiktoken.get_encoding("cl100k_base")
MAX_TOKENS=500
OVERLAP_TOKENS=80   

def token_count(text):
    return len(encoding.encode(text))

def split_by_tokens(text,max_tokens=MAX_TOKENS,overlap=OVERLAP_TOKENS):
    tokens=encoding.encode(text)
    
    if len(tokens)<=max_tokens:
        return [text]
    
    chunks=[]
    start=0
    while start<len(tokens):
        end=min(start+max_tokens,len(tokens))
        chunk_tokens=tokens[start:end]
        chunk=encoding.decode(chunk_tokens).strip()
        if chunk:
            chunks.append(chunk)
        if end>=len(tokens):
            break
        start=end-overlap
    return chunks

# CODE CHUNKING

def chunk_code_documents(document):
    code = document["text"]
    metadata = document["metadata"]
    chunks = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        for index, piece in enumerate(split_by_tokens(code)):
            chunks.append({
                "text": piece,
                "context": "",
                "metadata": {
                    **metadata,
                    "chunk_type": "code_fallback",
                    "chunk_index": index,
                },
            })
        return chunks

    # Keep imports and module-level statements as context.
    context_nodes = [
        node for node in tree.body
        if not isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        )
    ]
    context_parts = [
        segment
        for node in context_nodes
        if (segment := ast.get_source_segment(code, node))
    ]
    context = "\n\n".join(context_parts)

    structural_nodes = [
        node for node in tree.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        )
    ]

    # Files without top-level functions/classes remain searchable.
    if not structural_nodes:
        for index, piece in enumerate(split_by_tokens(code)):
            chunks.append({
                "text": piece,
                "context": "",
                "metadata": {
                    **metadata,
                    "chunk_type": "file",
                    "chunk_index": index,
                },
            })
        return chunks

    for node in structural_nodes:
        segment = ast.get_source_segment(code, node)
        if not segment:
            continue

        node_type = (
            "class" if isinstance(node, ast.ClassDef) else "function"
        )
        for index, piece in enumerate(split_by_tokens(segment)):
            chunks.append({
                "text": piece,
                "context": context,
                "metadata": {
                    **metadata,
                    "chunk_type": node_type,
                    "chunk_name": node.name,
                    "chunk_index": index,
                },
            })

    return chunks


def process_code_documents():
    chunks = []
    with open(CODE_INPUT, "r", encoding="utf-8") as f:
        for line in f:
            document = json.loads(line)
            document_chunks = chunk_code_documents(document)
            chunks.extend(document_chunks)

    with open(CODE_OUTPUT, "w", encoding="utf-8") as f:
        for index, chunk in enumerate(chunks):
            chunk["chunk_id"] = f"code_{index:06d}"
            f.write(
                json.dumps(
                    chunk,
                    ensure_ascii=False
                )
                + "\n"
            )
    return chunks

# THEORY CHUNKING
def split_theory_text(text):
    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []
    current = ""
    
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if token_count(candidate) <= MAX_TOKENS:
            current = candidate
            continue

        if current:
            chunks.append(current)

        if token_count(paragraph) > MAX_TOKENS:
            chunks.extend(split_by_tokens(paragraph))
            current = ""
        else:
            current = paragraph

    if current:
        chunks.append(current)
        
    # Add a small trailing context from the previous chunk.
    overlapped = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            overlapped.append(chunk)
            continue

        previous_tokens = encoding.encode(chunks[i - 1])
        overlap_text = encoding.decode(
            previous_tokens[-OVERLAP_TOKENS:]
        ).strip()
        overlapped.append(f"{overlap_text}\n\n{chunk}")

    return overlapped



def process_theory_documents():
    chunks = []
    with open(THEORY_INPUT, "r", encoding="utf-8") as f:
        for line in f:
            document = json.loads(line)
            pieces = split_theory_text(
                document["text"]
            )
            for index, piece in enumerate(pieces):
                chunks.append({
                    "chunk_id": "",
                    "text": piece,
                    "metadata": {
                        **document["metadata"],
                        "chunk_type": "theory",
                        "chunk_index": index
                    }
                })
                
    with open(THEORY_OUTPUT, "w", encoding="utf-8") as f:
        for index, chunk in enumerate(chunks):
            chunk["chunk_id"] = f"theory_{index:06d}"
            f.write(
                json.dumps(
                    chunk,
                    ensure_ascii=False
                )
                + "\n"
            )
    return chunks

# COMPLEXITY CHUNKING
def split_complexity_text(text):
    pattern = re.compile(
        r"(?m)^(?:list|collections\.deque|set|dict)\s*$",
        re.IGNORECASE
    )

    matches = list(pattern.finditer(text))
    sections = []

    # Keep the introductory content before the first section.
    if matches and text[:matches[0].start()].strip():
        sections.append(("overview", text[:matches[0].start()].strip()))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        heading = match.group().strip().lower()
        topic = {
            "list": "list_operations",
            "collections.deque": "deque_operations",
            "set": "set_operations",
            "dict": "dict_operations",
        }.get(heading, "python_operations")

        section_text = text[start:end].strip()

        if token_count(section_text) <= MAX_TOKENS:
            sections.append((topic, section_text))
        else:
            for piece in split_by_tokens(section_text):
                sections.append((topic, piece))

    return sections


def process_complexity_documents():
    chunks = []

    with open(COMPLEXITY_INPUT, "r", encoding="utf-8") as f:
        for line in f:
            document = json.loads(line)
            sections = split_complexity_text(document["text"])
            for index, (topic, piece) in enumerate(sections):
                chunks.append({
                    "chunk_id": "",
                    "text": piece,
                    "metadata": {
                        **document["metadata"],
                        "topic": topic,
                        "chunk_type": "complexity",
                        "chunk_index": index,
                    },
                })

    with open(COMPLEXITY_OUTPUT, "w", encoding="utf-8") as f:
        for index, chunk in enumerate(chunks):
            chunk["chunk_id"] = f"complexity_{index:06d}"
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    return chunks


# MAIN FUNCTION
if __name__ == "__main__":
    print("\n========== CODE ==========")
    code_chunks = process_code_documents()
    print(
        f"Code chunks created: {len(code_chunks)}"
    )
    print("\n========== THEORY ==========")
    theory_chunks = process_theory_documents()
    print(
        f"Theory chunks created: {len(theory_chunks)}"
    )
    print("\n========== COMPLEXITY ==========")
    complexity_chunks = process_complexity_documents()
    print(
        f"Complexity chunks created: "
        f"{len(complexity_chunks)}"
    )
    print("\n========== COMPLETE ==========")

    print(f"Code output: {CODE_OUTPUT}")
    print(f"Theory output: {THEORY_OUTPUT}")
    print(f"Complexity output: {COMPLEXITY_OUTPUT}")
    