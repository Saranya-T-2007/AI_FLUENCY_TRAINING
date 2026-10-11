import os
import sys


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from lc_config import get_vectorstore  

store = get_vectorstore()
questions = [
    "How much is the late fee for paying fees after the due date?",
    "What time should hostel students return?",
    "Can I write the exam with 70% attendance?",
]

for q in questions:
    print(f"\nQ: {q}")
    
    for doc, score in store.similarity_search_with_score(q, k=3):
        print(f"  {score:.3f}  [{doc.metadata['source']}]  {doc.page_content[:70]!r}")


print("\nFiltered to library.md:")
for doc in store.similarity_search("fine for late return", k=2, filter={"source": "library.md"}):
    print("  ", doc.metadata["source"], "->", doc.page_content[:80].replace("\n", " "))
