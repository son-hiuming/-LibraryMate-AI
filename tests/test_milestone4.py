"""Offline regression tests for Milestone 4.1 (Gemini network is never used)."""
import json

from langchain_core.messages import AIMessage
from src.guardrails.rules import check_tool, check_output
from src.agent import graph


def test_invalid_tool_arguments_are_rejected():
    assert check_tool('search_books', {'query': 'Python', 'limit': 0})
    assert check_tool('search_books', {'query': 'Python', 'limit': True})
    assert check_tool('search_library_policy', {'query': 'gia hạn', 'k': 99})
    assert check_tool('check_availability', {'book_id': '1'})
    assert check_tool('check_availability', {'book_id': 1, 'sql': 'DROP TABLE books'})
    assert check_tool('delete_database', {})
    assert check_tool('search_books', {'query': 'Python', 'limit': 5}) is None
    assert check_tool('search_library_policy', {'query': 'gia hạn', 'k': 3}) is None


def test_output_does_not_expose_gemini_signature():
    assert check_output([{'type':'text', 'text':'Chào bạn', 'extras':{'signature':'SECRET'}}]) == 'Chào bạn'


def test_budget_stops_extra_llm_tool_round(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE', 'gemini')
    calls = {'count': 0}

    class FakeLLM:
        def invoke(self, messages):
            calls['count'] += 1
            return AIMessage(content='', tool_calls=[{
                'name':'search_books', 'args':{'query':'Python'}, 'id':f'call-{calls["count"]}'
            }])

    monkeypatch.setattr(graph, '_get_llm', lambda: FakeLLM())
    # Avoid involving the database in this graph budget test.
    class FakeTool:
        def invoke(self, args):
            return json.dumps({'books': []})
    monkeypatch.setitem(graph.TOOL_MAP, 'search_books', FakeTool())
    result = graph.ask('Tìm Python')
    assert calls['count'] == graph.MAX_LLM_CALLS
    assert result['steps'] == graph.MAX_LLM_CALLS
    assert result['tool_calls'] == 2
    assert 'giới hạn' in result['answer'].lower()


def test_rate_limit_is_user_friendly_and_logged(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE', 'gemini')
    class GoogleRateLimitError(Exception):
        pass
    class FakeLLM:
        def invoke(self, messages):
            raise GoogleRateLimitError('Sensitive raw provider error')
    monkeypatch.setattr(graph, '_get_llm', lambda: FakeLLM())
    events=[]
    monkeypatch.setattr(graph, 'record_event', lambda run_id, event, **fields: events.append((event, fields)))
    result=graph.ask('Gia hạn sách thế nào?')
    assert 'giới hạn' in result['answer']
    assert result['steps'] is None
    assert 'Sensitive raw' not in result['answer']
    assert any(name=='llm_error' for name,_ in events)
    assert any(name=='completed' and fields['error_type']=='GoogleRateLimitError' for name,fields in events)


def test_large_tool_batch_is_stopped_without_execution(monkeypatch):
    monkeypatch.setenv('LIBRARYMATE_MODE','gemini')
    class FakeLLM:
        def invoke(self, messages):
            return AIMessage(content='',tool_calls=[
                {'name':'search_books','args':{'query':'Python'},'id':f'b{i}'}
                for i in range(graph.MAX_TOOLS_PER_TURN+1)
            ])
    monkeypatch.setattr(graph, '_get_llm', lambda: FakeLLM())
    result=graph.ask('Tìm sách Python')
    assert 'giới hạn' in result['answer'].lower()
    assert result['tool_calls'] == 0
    assert result['steps'] == 1
