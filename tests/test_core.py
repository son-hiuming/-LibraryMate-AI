import json
import sqlite3
from scripts.init_db import init_database,DB
from src.guardrails.rules import check_input,check_tool
from src.tools.library_tools import search_books,check_availability,search_library_policy

def setup_module():init_database()

def test_seed_count():
    with sqlite3.connect(DB) as con:
        assert con.execute('SELECT COUNT(*) FROM books').fetchone()[0]==150

def test_python_search():
    r=json.loads(search_books.invoke({'query':'Python'}))
    assert r['books'] and any('Python' in b['title'] for b in r['books'])

def test_stock_zero():
    r=json.loads(check_availability.invoke({'book_id':2}))
    assert r['book']['available_copies']==0

def test_policy_retrieval(monkeypatch):
    from src.rag import engine
    monkeypatch.setattr(engine,'retrieve', lambda q,k=3: {'query':q,'passages':[{'section':'P02','text':'14 ngày'}], 'retrieval':'semantic_chroma'})
    r=json.loads(search_library_policy.invoke({'query':'thời hạn mượn bao nhiêu ngày'}))
    assert any('P02' in p['section'] for p in r['passages'])

def test_guardrails():
    assert check_input('DROP TABLE books') is not None
    assert check_tool('delete_books',{}) is not None
    assert check_tool('search_books',{'query':'Python'}) is None

def test_demo_graph(monkeypatch):
    from src.rag import engine
    monkeypatch.setattr(engine,'retrieve', lambda q,k=3: {'query':q,'passages':[], 'retrieval':'semantic_chroma'})
    monkeypatch.setenv('LIBRARYMATE_MODE','demo')
    from src.agent.graph import ask
    r=ask('Tìm sách Python')
    assert 'Python' in r['answer'] and r['steps']>=2

def test_blocked_graph(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE','demo')
    from src.agent.graph import ask
    r=ask('DROP TABLE books')
    assert 'không được phép' in r['answer']


def test_book_id_graph(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE','demo')
    from src.agent.graph import ask
    r=ask('Sách có mã 2 còn không?')
    assert '0/3' in r['answer']


def test_catalog_multiple_subjects():
    with sqlite3.connect(DB) as con:
        assert con.execute('SELECT COUNT(DISTINCT category) FROM books').fetchone()[0] >= 15
        assert con.execute('SELECT COUNT(*) FROM books WHERE available_copies > total_copies OR available_copies < 0').fetchone()[0] == 0

def test_vietnamese_topic_search():
    result = json.loads(search_books.invoke({'query':'marketing'}))
    assert result['books'] and any('Marketing' in b['category'] for b in result['books'])


def test_policy_only_does_not_search_catalog(monkeypatch):
    from src.rag import engine
    monkeypatch.setattr(engine,'retrieve', lambda q,k=3: {'query':q,'passages':[{'section':'P03','text':'Gia hạn một lần'}], 'retrieval':'semantic_chroma'})
    monkeypatch.setenv('LIBRARYMATE_MODE','demo')
    from src.agent.graph import _demo_initial, ask
    calls = _demo_initial('Gia hạn sách thế nào?').tool_calls
    assert [c['name'] for c in calls] == ['search_library_policy']
    answer = ask('Gia hạn sách thế nào?')['answer']
    assert '**Sách tìm thấy:**' not in answer
    assert 'P03' in answer

def test_combined_query_uses_two_tools(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE','demo')
    from src.agent.graph import _demo_initial
    names = [c['name'] for c in _demo_initial('Tìm sách SQL và thời hạn mượn?').tool_calls]
    assert names == ['search_books','search_library_policy']


def test_policy_chunk_ids():
    from src.rag.engine import policy_chunks
    chunks=policy_chunks()
    assert [c["id"] for c in chunks]==[f"P{i:02}" for i in range(1,8)]
    assert all("Quy định tiếng Việt:" in c["text"] for c in chunks)

def test_output_gemini_blocks():
    from src.guardrails.rules import check_output
    assert check_output([{"type":"text","text":"Xin chào!","extras":{"signature":"secret"}}])=="Xin chào!"

def test_rag_validation():
    from src.rag.engine import retrieve
    import pytest
    with pytest.raises(ValueError): retrieve("", k=3)
    with pytest.raises(ValueError): retrieve("Gia hạn", k=0)
