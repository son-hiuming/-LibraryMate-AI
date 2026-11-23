"""Read-only tools. The policy retriever is keyword-based in Milestone 2;
semantic vector RAG will be added in Milestone 3."""
from pathlib import Path
import json
import re
import sqlite3
import unicodedata
from langchain_core.tools import tool

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "library.db"
POLICY = ROOT / "data" / "library_policy.md"


def _normalize(s):
    s = unicodedata.normalize('NFD', str(s).lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def _get_db():
    if not DB.exists():
        raise RuntimeError('Database not initialized; run python -m scripts.init_db')
    return sqlite3.connect(f'file:{DB}?mode=ro', uri=True)


@tool

def search_books(query: str, limit: int = 5) -> str:
    """Find catalog books by title, topic, author or learning need. Read only."""
    if not query.strip() or len(query) > 200 or not 1 <= limit <= 10:
        raise ValueError('Invalid query or limit')
    tokens = [t for t in _normalize(query).split() if len(t)>2]
    synonyms = {'lap':'python','trinh':'python','co':'database','du':'database','lieu':'database',
                'sql':'database','thuat':'algorithms','toan':'algorithms'}
    terms = list(dict.fromkeys(tokens + [synonyms[t] for t in tokens if t in synonyms]))
    with _get_db() as con:
        con.row_factory = sqlite3.Row
        rows = [dict(r) for r in con.execute('SELECT * FROM books')]
    def score(book):
        title = _normalize(book['title'])
        fields = _normalize(' '.join(str(book[k]) for k in ['title','author','category','description']))
        return sum((3 if t in title else 1) for t in terms if t in fields)
    scored = sorted([(score(b),b) for b in rows], key=lambda x:(-x[0], x[1]['book_id']))
    results = [book for score_,book in scored if score_>0][:limit]
    return json.dumps({'query':query,'books':results,'source':'fictional_sqlite_catalog'},ensure_ascii=False)


@tool

def check_availability(book_id: int) -> str:
    """Look up exact number of available copies for a book_id, read-only."""
    if not 1 <= book_id <= 1000000:
        raise ValueError('Invalid book_id')
    with _get_db() as con:
        con.row_factory = sqlite3.Row
        row = con.execute('SELECT book_id,title,available_copies,total_copies,shelf_location FROM books WHERE book_id=?',(book_id,)).fetchone()
    return json.dumps({'book':dict(row) if row else None, 'source':'fictional_sqlite_catalog'},ensure_ascii=False)



@tool
def search_library_policy(query: str, k: int = 3) -> str:
    """SEMANTIC RAG for fictional library rules. Return citeable P01-P07 evidence. Query may be Vietnamese."""
    from src.rag.engine import retrieve
    return json.dumps(retrieve(query, k=k), ensure_ascii=False)

TOOLS = [search_books, check_availability, search_library_policy]
TOOL_MAP = {t.name: t for t in TOOLS}
