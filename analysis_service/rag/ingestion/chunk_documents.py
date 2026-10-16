from pathlib import Path
import ast
import hashlib
import json
import re
import tiktoken

BASE = Path(__file__).resolve().parents[1] / "knowledge" / "dsa" / "processed"

CODE_INPUT = BASE / "documents/code_documents.jsonl"
THEORY_INPUT = BASE / "documents/theory_documents.jsonl"
COMPLEXITY_INPUT = BASE / "documents/python_complexity.jsonl"

OUTPUT_DIR = BASE / "chunks"

CODE_OUTPUT = OUTPUT_DIR / "code/code_chunks.jsonl"
THEORY_OUTPUT = OUTPUT_DIR / "theory/theory_chunks.jsonl"
COMPLEXITY_OUTPUT = OUTPUT_DIR / "complexity/complexity_chunks.jsonl"
ALGORITHM_COMPLEXITY_INPUT = (BASE / "documents" / "dsa_algorithm_complexity.jsonl")
ALGORITHM_COMPLEXITY_OUTPUT = (OUTPUT_DIR/ "algorithm_complexity"/ "algorithm_complexity_chunks.jsonl")
MAX_TOKENS = 500
OVERLAP_TOKENS = 50

encoding = tiktoken.get_encoding("cl100k_base")

def token_count(text):
    return len(encoding.encode(text))

def split_by_tokens(text, max_tokens=MAX_TOKENS, overlap=0):
    """Fallback for text that cannot be split structurally."""
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0
    step = max(1, max_tokens - overlap)

    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        piece = encoding.decode(tokens[start:end]).strip()

        if piece:
            chunks.append(piece)

        if end == len(tokens):
            break

        start += step

    return chunks

def read_jsonl(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path.resolve()}"
        )

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path}, line {line_number}"
                ) from exc

def write_jsonl(path, chunks, prefix):
    """Write deterministic IDs and fresh output files."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for index, chunk in enumerate(chunks):
            chunk["chunk_id"] = f"{prefix}_{index:06d}"

            # Record the size of the searchable text.
            chunk["metadata"]["token_count"] = token_count(
                chunk["text"]
            )
            file.write(
                json.dumps(chunk, ensure_ascii=False) + "\n"
            )

def stable_source_id(metadata):
    """Useful for tracing chunks back to their source."""
    identity = "|".join(
        str(metadata.get(key, ""))
        for key in ("source", "path", "filename", "category")
    )
    return hashlib.sha1(
        identity.encode("utf-8")
    ).hexdigest()[:12]

# ============================================================
# CODE CHUNKING: AST-AWARE
# ============================================================
STRUCTURAL_TYPES = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
)

def node_start_line(node):
    decorators = getattr(node, "decorator_list", [])
    if decorators:
        return min(node.lineno, *(d.lineno for d in decorators))
    return node.lineno

def node_segment(source, node):
    """Preserve decorators when extracting a function or class."""
    lines = source.splitlines()
    start = node_start_line(node)
    end = getattr(node, "end_lineno", node.lineno)

    return "\n".join(lines[start - 1:end]).strip()

def module_context(source, tree):
    """Keep imports, module docstrings and global setup as context."""
    parts = []

    for node in tree.body:
        if isinstance(node, STRUCTURAL_TYPES):
            continue

        segment = node_segment(source, node)
        if segment:
            parts.append(segment)

    return "\n\n".join(parts)

def split_large_function(source, node):
    """
    Preserve the function signature and group complete body statements.
    Token splitting is only a fallback for a single oversized statement.
    """
    segment = node_segment(source, node)

    if token_count(segment) <= MAX_TOKENS:
        return [(segment, node.name, "function")]

    if not getattr(node, "body", None):
        return [
            (piece, node.name, "code_fallback")
            for piece in split_by_tokens(segment)
        ]

    lines = source.splitlines()
    start = node_start_line(node)
    first_body_line = min(
        node_start_line(child) for child in node.body
    )

    # Function declaration, decorators and signature.
    header = "\n".join(
        lines[start - 1:first_body_line - 1]
    ).rstrip()

    chunks = []
    current_statements = []

    def emit(statements):
        if not statements:
            return

        body = "\n\n".join(statements)
        text = f"{header}\n{body}".strip()

        chunks.append((text, node.name, "function_fragment"))

    for statement in node.body:
        statement_text = node_segment(source, statement)
        candidate_statements = current_statements + [statement_text]
        candidate = (
            f"{header}\n"
            + "\n\n".join(candidate_statements)
        ).strip()

        if token_count(candidate) <= MAX_TOKENS:
            current_statements.append(statement_text)
            continue

        emit(current_statements)
        current_statements = []

        single_candidate = f"{header}\n{statement_text}".strip()

        if token_count(single_candidate) <= MAX_TOKENS:
            current_statements = [statement_text]
        else:
            # Last resort: a very large individual statement.
            for piece in split_by_tokens(statement_text):
                chunks.append((
                    f"{header}\n{piece}".strip(),
                    node.name,
                    "code_fallback",
                ))

    emit(current_statements)
    return chunks

def chunk_code_documents(document):
    source = document["text"]
    metadata = document["metadata"]

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [{
            "text": piece,
            "context": "",
            "metadata": {
                **metadata,
                "source_id": stable_source_id(metadata),
                "chunk_type": "code_fallback",
            },
        } for piece in split_by_tokens(source)]

    context = module_context(source, tree)
    structural_nodes = [
        node for node in tree.body
        if isinstance(node, STRUCTURAL_TYPES)
    ]

    # Files containing only executable statements or expressions.
    if not structural_nodes:
        pieces = split_by_tokens(source)
        return [{
            "text": piece,
            "context": "",
            "metadata": {
                **metadata,
                "source_id": stable_source_id(metadata),
                "chunk_type": "file",
            },
        } for piece in pieces]

    chunks = []

    for node in structural_nodes:
        segment = node_segment(source, node)
        if token_count(segment) <= MAX_TOKENS:
            pieces = [(segment, node.name,
                       "class" if isinstance(node, ast.ClassDef)
                       else "function")]
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            pieces = split_large_function(source, node)
        else:
            # Oversized class: preserve the class declaration as context
            # and index its members separately where possible.
            class_lines = source.splitlines()
            first_member_line = min(
                node_start_line(child) for child in node.body
            ) if node.body else node.end_lineno

            class_header = "\n".join(
                class_lines[node_start_line(node) - 1:
                            first_member_line - 1]
            ).strip()

            pieces = []
            if not node.body:
                pieces = [
                    (piece, node.name, "code_fallback")
                    for piece in split_by_tokens(segment)
                ]
            else:
                for member in node.body:
                    member_text = node_segment(source, member)
                    if isinstance(
                        member, (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        member_pieces = split_large_function(
                            source, member
                        )
                    else:
                        member_pieces = [(
                            member_text,
                            getattr(member, "name", node.name),
                            "class_member",
                        )]
                    for piece, name, kind in member_pieces:
                        pieces.append((
                            piece,
                            name,
                            "class_member" if kind == "function"
                            else kind,
                        ))

            # Store class declaration separately as supporting context.
            for piece, name, kind in pieces:
                chunks.append({
                    "text": piece,
                    "context": "\n\n".join(
                        part for part in (context, class_header)
                        if part
                    ),
                    "metadata": {
                        **metadata,
                        "source_id": stable_source_id(metadata),
                        "chunk_type": kind,
                        "chunk_name": name,
                    },
                })
            continue

        for piece, name, kind in pieces:
            chunks.append({
                "text": piece,
                "context": context,
                "metadata": {
                    **metadata,
                    "source_id": stable_source_id(metadata),
                    "chunk_type": kind,
                    "chunk_name": name,
                },
            })
    return chunks

def process_code_documents():
    chunks = []
    for document in read_jsonl(CODE_INPUT):
        chunks.extend(chunk_code_documents(document))
    write_jsonl(CODE_OUTPUT, chunks, "code")
    return chunks

# ============================================================
# THEORY CHUNKING: HEADING + PARAGRAPH + SENTENCE AWARE
# ============================================================
HEADING_PATTERNS = [
    re.compile(r"^(?:lecture|chapter|section)\s+\d+\b", re.I),
    re.compile(r"^\d+(?:\.\d+)*[.)]?\s+\S"),
    re.compile(r"^[A-Z][A-Z0-9\s:&()-]{2,65}$"),
]
BULLET_PATTERN = re.compile(
    r"^(?:[-*•▪]|\d+[.)])\s+"
)

def is_theory_heading(line):
    line = line.strip()
    if not line or len(line) > 100:
        return False

    if line.endswith((".", "?", "!", ";")):
        return False

    if any(pattern.match(line) for pattern in HEADING_PATTERNS):
        return True
    # Only recognize explicit structural heading patterns.
    # Avoid treating ordinary short PDF lines as headings.
    return False

def split_oversized_paragraph(text):
    """Split at sentence boundaries before falling back to token windows."""
    if token_count(text) <= MAX_TOKENS:
        return [text.strip()]

    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())

    if len(sentences) <= 1:
        return split_by_tokens(text, MAX_TOKENS, overlap=0)

    chunks = []
    current = ""

    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence

        if token_count(candidate) <= MAX_TOKENS:
            current = candidate
            continue

        if current:
            chunks.append(current)

        if token_count(sentence) > MAX_TOKENS:
            chunks.extend(
                split_by_tokens(sentence, MAX_TOKENS, overlap=0)
            )
            current = ""
        else:
            current = sentence

    if current:
        chunks.append(current)

    return chunks

def extract_theory_blocks(text):
    """
    Rejoin wrapped PDF lines into readable paragraphs.
    Keep headings and list items recognizable.
    """
    lines = [line.strip() for line in text.splitlines()]
    blocks = []
    paragraph_lines = []

    def flush_paragraph():
        if paragraph_lines:
            blocks.append(("paragraph", " ".join(paragraph_lines)))
            paragraph_lines.clear()

    for line in lines:
        if not line:
            flush_paragraph()
            continue

        if is_theory_heading(line):
            flush_paragraph()
            blocks.append(("heading", line))
            continue

        if BULLET_PATTERN.match(line):
            flush_paragraph()
            blocks.append(("list_item", line))
            continue

        paragraph_lines.append(line)

    flush_paragraph()
    return blocks

def split_theory_text(text):
    blocks = extract_theory_blocks(text)

    chunks = []
    current = ""
    active_heading = ""

    def flush():
        nonlocal current
        if current.strip():
            chunks.append(current.strip())
        current = ""

    for block_type, content in blocks:
        if block_type == "heading":
            # Keep consecutive headings together with the following content.
            if current and token_count(current) > 100:
                flush()
            active_heading = (
                f"{active_heading}\n{content}".strip()
                if current and token_count(current) <= 100
                else content
            )
            current = active_heading
            continue

        # Keep list items and prose grouped when they fit.
        candidate = (
            f"{current}\n{content}" if current else content
        )

        if token_count(candidate) <= MAX_TOKENS:
            current = candidate
            continue

        flush()

        if token_count(content) <= MAX_TOKENS:
            # Repeat the section heading when a new chunk is needed.
            prefix = active_heading
            candidate = f"{prefix}\n{content}".strip() if prefix else content

            if token_count(candidate) <= MAX_TOKENS:
                current = candidate
            else:
                current = content
        else:
            pieces = split_oversized_paragraph(content)

            for piece_index, piece in enumerate(pieces):
                prefix = active_heading if piece_index == 0 else active_heading
                candidate = f"{prefix}\n{piece}".strip() if prefix else piece

                if token_count(candidate) <= MAX_TOKENS:
                    chunks.append(candidate)
                else:
                    chunks.extend(
                        split_by_tokens(piece, MAX_TOKENS, overlap=0)
                    )

    flush()
    return chunks

def process_theory_documents():
    chunks = []

    for document in read_jsonl(THEORY_INPUT):
        pieces = split_theory_text(document["text"])

        for index, piece in enumerate(pieces):
            chunks.append({
                "text": piece,
                "metadata": {
                    **document["metadata"],
                    "source_id": stable_source_id(
                        document["metadata"]
                    ),
                    "chunk_type": "theory",
                    "local_chunk_index": index,
                },
            })

    write_jsonl(THEORY_OUTPUT, chunks, "theory")
    return chunks

# ============================================================
# COMPLEXITY CHUNKING: OPERATION-SECTION AWARE
# ============================================================
COMPLEXITY_HEADINGS = {
    "list": "list_operations",
    "collections.deque": "deque_operations",
    "set": "set_operations",
    "dict": "dict_operations",
}

COMPLEXITY_PATTERN = re.compile(
    r"(?im)^[ \t]*(list|collections\.deque|set|dict)[ \t]*$"
)

def split_complexity_text(text):
    matches = list(COMPLEXITY_PATTERN.finditer(text))
    sections = []

    if not matches:
        return [("python_operations", piece)
                for piece in split_by_tokens(text)]

    intro = text[:matches[0].start()].strip()
    if intro:
        sections.append(("overview", intro))

    for index, match in enumerate(matches):
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        heading = match.group(1).lower()
        topic = COMPLEXITY_HEADINGS[heading]
        section = text[start:end].strip()

        # Prefer paragraph boundaries for large sections.
        paragraphs = [
            part.strip()
            for part in re.split(r"\n\s*\n", section)
            if part.strip()
        ]

        current = ""
        for paragraph in paragraphs:
            candidate = (
                f"{current}\n\n{paragraph}"
                if current else paragraph
            )
            if token_count(candidate) <= MAX_TOKENS:
                current = candidate
                continue
            if current:
                sections.append((topic, current))
            if token_count(paragraph) > MAX_TOKENS:
                sections.extend(
                    (topic, piece)
                    for piece in split_by_tokens(paragraph)
                )
                current = ""
            else:
                current = paragraph

        if current:
            sections.append((topic, current))
    return sections

def process_complexity_documents():
    chunks = []

    for document in read_jsonl(COMPLEXITY_INPUT):
        sections = split_complexity_text(document["text"])
        for index, (topic, piece) in enumerate(sections):
            chunks.append({
                "text": piece,
                "metadata": {
                    **document["metadata"],
                    "source_id": stable_source_id(
                        document["metadata"]
                    ),
                    "topic": topic,
                    "chunk_type": "complexity",
                    "local_chunk_index": index,
                },
            })
    write_jsonl(COMPLEXITY_OUTPUT, chunks, "complexity")
    return chunks

# ============================================================
# ALGORITHM COMPLEXITY CHUNKING
# ============================================================

def process_algorithm_complexity_documents():
    chunks = []
    for document in read_jsonl(ALGORITHM_COMPLEXITY_INPUT):
        text = document.get("text", "").strip()

        if not text:
            raise ValueError(
                f"Empty algorithm-complexity document: {document}"
            )
        # Support both flat JSONL records and nested metadata records.
        if isinstance(document.get("metadata"), dict):
            metadata = dict(document["metadata"])
        else:
            metadata = {
                key: value
                for key, value in document.items()
                if key != "text"
            }

        if not metadata.get("topic"):
            raise ValueError(
                "Every algorithm-complexity record must have a topic."
            )
        # Each record is already a focused explanation.
        # Split only if it exceeds the configured token limit.
        pieces = split_oversized_paragraph(text)
        for index, piece in enumerate(pieces):
            chunks.append({
                "text": piece,
                "metadata": {
                    **metadata,
                    "source_id": hashlib.sha1(
                        (
                            str(metadata.get("source", ""))
                            + "|"
                            + str(metadata["topic"])
                        ).encode("utf-8")
                    ).hexdigest()[:12],
                    "chunk_type": "algorithm_complexity",
                    "local_chunk_index": index,
                },
            })

    write_jsonl(
        ALGORITHM_COMPLEXITY_OUTPUT,
        chunks,
        "algorithm",
    )
    return chunks

if __name__ == "__main__":
    print("\n========== CODE ==========")
    code_chunks = process_code_documents()
    print(f"Code chunks created: {len(code_chunks)}")

    print("\n========== THEORY ==========")
    theory_chunks = process_theory_documents()
    print(f"Theory chunks created: {len(theory_chunks)}")

    print("\n========== COMPLEXITY ==========")
    complexity_chunks = process_complexity_documents()
    print(f"Complexity chunks created: {len(complexity_chunks)}")

    print("\n========== ALGORITHM COMPLEXITY ==========")
    algorithm_chunks = process_algorithm_complexity_documents()
    print(f"Algorithm complexity chunks created: {len(algorithm_chunks)}")

    print("\n========== COMPLETE ==========")
    print(f"Code output: {CODE_OUTPUT}")
    print(f"Theory output: {THEORY_OUTPUT}")
    print(f"Complexity output: {COMPLEXITY_OUTPUT}")
    print(f"Algorithm output: {ALGORITHM_COMPLEXITY_OUTPUT}")