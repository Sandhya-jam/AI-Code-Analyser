
from retrieval.retriever import retrieve

questions = [
    "Binary search takes logarithmic time because it halves the search interval.",
    "What is the time complexity of binary search in a sorted array?",
]

for question in questions:
    print("\nQUESTION:", question)

    for rank, result in enumerate(
        retrieve(question, top_k=5, knowledge_type="theory"),
        start=1,
    ):
        print(f"\nRank {rank} | Distance: {result['distance']:.4f}")
        print("File:", result["metadata"].get("filename"))
        print(result["text"][:500])