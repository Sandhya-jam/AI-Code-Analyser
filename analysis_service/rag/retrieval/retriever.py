from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

RAG_DIR = Path(__file__).resolve().parent.parent
DB_DIR = RAG_DIR / "chroma"
COLLECTION_NAME = "dsa_knowledge"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

def retrieve(query, top_k=5, category=None, knowledge_type=None):
    filters = []

    if category:
        filters.append({"category": category})

    if knowledge_type:
        filters.append({"type": knowledge_type})

    where = None
    if len(filters) == 1:
        where = filters[0]
    elif len(filters) > 1:
        where = {"$and": filters}

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for i, text in enumerate(results["documents"][0]):
        matches.append({
            "text": text,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches


def retrieve_expanded(query, top_k=5, knowledge_type=None):
    expansions = {
        "binary search": [
            "binary search time complexity O(log n)",
            "binary search repeatedly halves the sorted search interval",
        ],
        "both ends": [
            "collections.deque append appendleft pop popleft O(1)",
            "double ended queue efficient insertion and removal at both ends",
        ],
    }

    queries = [query]
    query_lower = query.lower()

    for phrase, variants in expansions.items():
        if phrase in query_lower:
            queries.extend(variants)

    # Merge results by chunk ID, keeping the best distance.
    unique = {}

    for expanded_query in queries:
        matches = retrieve(
            expanded_query,
            top_k=top_k,
            knowledge_type=knowledge_type,
        )

        for match in matches:
            chunk_id = match["metadata"]["chunk_id"]
            if (
                chunk_id not in unique
                or match["distance"] < unique[chunk_id]["distance"]
            ):
                unique[chunk_id] = match

    return sorted(
        unique.values(),
        key=lambda match: match["distance"],
    )[:top_k]

if __name__ == "__main__":
    tests = [
        {
            "question": "What is the time complexity of binary search?",
            "type": "theory",
        },
        {
            "question": (
                "Which Python data structure supports efficient "
                "insertion and removal at both ends?"
            ),
            "type": "complexity",
        },
        {
            "question": "Find a Python implementation of binary search.",
            "type": "code",
        },
    ]

    # for test in tests:
    #     print("\n" + "=" * 70)
    #     print("QUESTION:", test["question"])
    #     print("KNOWLEDGE TYPE:", test["type"])

    #     results = retrieve_expanded(
    #         test["question"],
    #         top_k=5,
    #         knowledge_type=test["type"],
    #     )

    #     for rank, match in enumerate(results, start=1):
    #         print(f"\nRank {rank} | Distance: {match['distance']:.4f}")
    #         print("Source:", match["metadata"].get("source"))
    #         print("Topic:", match["metadata"].get("topic"))
    #         print("Category:", match["metadata"].get("category"))
    #         print("Text:", match["text"][:500])
    results = retrieve_expanded(
        "What is the time complexity of binary search?",
        top_k=5,
    )
    for rank, match in enumerate(results, start=1):
        print(f"\nRank {rank} | Distance: {match['distance']:.4f}")
        print("Source:", match["metadata"].get("source"))
        print("Topic:", match["metadata"].get("topic"))
        print("Category:", match["metadata"].get("category"))
        print("Text:", match["text"][:500])