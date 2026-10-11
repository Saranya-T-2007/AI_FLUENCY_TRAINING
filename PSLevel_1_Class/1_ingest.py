import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_config import DB_DIR, EMBED_PROVIDER, get_vectorstore 


script_dir = Path(__file__).resolve().parent
possible_paths = [
    script_dir / "data",          
    script_dir.parent / "data",   
    Path("data")                  
]

data_dir = None
for p in possible_paths:
    if p.exists() and p.is_dir():
        data_dir = p
        break

if not data_dir:
    raise FileNotFoundError(
        "Could not find the 'data' directory anywhere! "
        f"Checked locations: {[str(p) for p in possible_paths]}"
    )

print(f"Reading files from: {data_dir.resolve()}")

docs = []
for path in sorted(data_dir.glob("*.md")):
    docs.append(Document(page_content=path.read_text(encoding="utf-8"),
                         metadata={"source": path.name}))
print(f"Loaded {len(docs)} documents")


splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks (chunk_size=300, overlap=50)")


print("Example chunk ->", repr(chunks[4].page_content[:120]), chunks[4].metadata)

shutil.rmtree(DB_DIR, ignore_errors=True)
store = get_vectorstore()
ids = store.add_documents(chunks)
print(f"Stored {len(ids)} vectors in ./{DB_DIR} using EMBED_PROVIDER={EMBED_PROVIDER}")
print("Vector length:", len(store.embeddings.embed_query("test")))
