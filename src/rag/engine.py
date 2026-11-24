"""Bilingual library policy RAG with local SentenceTransformers + Chroma.

Build the index once using `python -m scripts.build_rag_index` before running.
The index stores seven sections as separate citeable chunks, not an LLM-generated answer.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / 'data' / 'library_policy.md'
INDEX_PATH = ROOT / 'data' / 'chroma_db'
COLLECTION = 'library_policy_v1'
DEFAULT_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'


def model_name() -> str:
    return os.getenv('RAG_EMBEDDING_MODEL', DEFAULT_MODEL)


def policy_chunks(path: Path = POLICY_PATH) -> list[dict]:
    """One chunk per Pxx section; include both original English and Vietnamese explanation."""
    content = path.read_text(encoding='utf8')
    blocks = re.findall(r'(?ms)^##\s+(P\d+)\s*[—–-]\s*([^\n]+)\n(.*?)(?=^##\s+P\d+|\Z)', content)
    if not blocks:
        raise ValueError(f'No policy sections found in {path}')
    chunks=[]
    for section,title,body in blocks:
        chunks.append({'id':section, 'section': section, 'title': title.strip(),
                       'text': body.strip(), 'source': 'data/library_policy.md'})
    return chunks


def _fingerprint(chunks: list[dict], model: str) -> str:
    content = model + '\n' + '\n'.join(c['id']+'\n'+c['text'] for c in chunks)
    return hashlib.sha256(content.encode('utf8')).hexdigest()


@lru_cache(maxsize=2)
def _encoder(name: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name)


@lru_cache(maxsize=1)
def _db():
    """Reuse one Chroma client per Python process.

    Constructing PersistentClient for each question adds avoidable overhead.
    The index is still read from the same local persistent directory; this
    cache does not cache answers or skip freshness checks in retrieve().
    """
    import chromadb
    INDEX_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(INDEX_PATH))


def build_index(force: bool = False) -> dict:
    """Create/update Chroma collection; no network/API key beyond initial model download."""
    chunks=policy_chunks()
    model=model_name()
    marker=_fingerprint(chunks,model)
    client=_db()
    collection=client.get_or_create_collection(name=COLLECTION,metadata={'hnsw:space':'cosine'})
    existing=collection.get(include=['metadatas'])
    metadata=existing.get('metadatas') or []
    valid=(len(existing['ids']) == len(chunks) and all((m or {}).get('fingerprint')==marker for m in metadata))
    if valid and not force:
        return {'status':'already_current','chunks':len(chunks),'model':model,'path':str(INDEX_PATH)}
    vectors=_encoder(model).encode([f"{c['section']} {c['title']}. {c['text']}" for c in chunks],normalize_embeddings=True,show_progress_bar=False).tolist()
    # Update atomically at collection level enough for a local, single-user demo.
    if existing['ids']:collection.delete(ids=existing['ids'])
    collection.add(ids=[c['id'] for c in chunks],embeddings=vectors,
                   documents=[c['text'] for c in chunks],
                   metadatas=[{'section':c['section'],'title':c['title'],'source':c['source'],
                               'fingerprint':marker,'embedding_model':model} for c in chunks])
    return {'status':'indexed','chunks':len(chunks),'model':model,'path':str(INDEX_PATH)}


def retrieve(query: str, k: int = 3, max_distance: float = 0.75) -> dict:
    """Semantic cosine retrieval; low similarity is rejected rather than invented.

    Returns source-tagged passages. A missing/stale index is an explicit error.
    """
    if not isinstance(query,str) or not query.strip() or len(query)>200:
        raise ValueError('Policy query must be 1..200 characters')
    if not isinstance(k,int) or not 1<=k<=5:
        raise ValueError('k must be an integer from 1 to 5')
    client=_db()
    try:collection=client.get_collection(name=COLLECTION)
    except Exception as exc:
        raise RuntimeError('RAG index missing. Run: python -m scripts.build_rag_index') from exc
    chunks=policy_chunks(); marker=_fingerprint(chunks,model_name())
    check=collection.get(limit=1,include=['metadatas'])
    if collection.count()!=len(chunks) or not check['metadatas'] or check['metadatas'][0].get('fingerprint')!=marker:
        raise RuntimeError('RAG index outdated. Run: python -m scripts.build_rag_index --force')
    vector=_encoder(model_name()).encode([query],normalize_embeddings=True,show_progress_bar=False)[0].tolist()
    result=collection.query(query_embeddings=[vector],n_results=min(k,len(chunks)),include=['documents','metadatas','distances'])
    passages=[]
    for doc,meta,distance in zip(result['documents'][0],result['metadatas'][0],result['distances'][0]):
        if float(distance)>max_distance:continue
        passages.append({'section':meta['section'], 'title':meta['title'], 'text':doc,
                         'source':meta['source'], 'score':round(1-float(distance),3)})
    return {'query':query,'retrieval':'semantic_chroma','embedding_model':model_name(), 'passages':passages}
