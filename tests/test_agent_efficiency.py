"""Offline regression tests for API-saving LangGraph changes."""
import json

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from src.agent import graph


def test_greeting_does_not_call_gemini(monkeypatch):
    monkeypatch.setenv("LIBRARYMATE_MODE", "gemini")
    monkeypatch.setattr(graph, "_get_llm", lambda: (_ for _ in ()).throw(AssertionError("LLM should not be called")))
    monkeypatch.setattr(graph, "record_event", lambda *args, **kwargs: None)
    result = graph.agent({
        "messages": [HumanMessage(content="Xin chào!")],
        "run_id": "test-greeting", "steps": 0, "tool_count": 0,
    })
    assert "LibraryMate AI" in result["messages"][0].content
    assert result["steps"] == 0


def test_business_question_still_calls_llm(monkeypatch):
    monkeypatch.setenv("LIBRARYMATE_MODE", "gemini")
    monkeypatch.setattr(graph, "record_event", lambda *args, **kwargs: None)

    class FakeLLM:
        def invoke(self, messages):
            return AIMessage(content="Tôi cần tra cứu trước.")

    monkeypatch.setattr(graph, "_get_llm", lambda: FakeLLM())
    result = graph.agent({
        "messages": [HumanMessage(content="Tìm sách Python")],
        "run_id": "test-business", "steps": 0, "tool_count": 0,
    })
    assert result["steps"] == 1


def test_duplicate_tool_batch_only_executes_once(monkeypatch):
    calls = []

    class FakeTool:
        def invoke(self, args):
            calls.append(args)
            return json.dumps({"books": [], "query": args["query"]})

    monkeypatch.setattr(graph, "record_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(graph, "check_tool", lambda name, args: None)
    monkeypatch.setitem(graph.TOOL_MAP, "search_books", FakeTool())
    response = AIMessage(content="", tool_calls=[
        {"name": "search_books", "args": {"query": "Python"}, "id": "one"},
        {"name": "search_books", "args": {"query": "Python"}, "id": "two"},
    ])
    result = graph.run_tools({"messages": [response], "run_id": "test-duplicate", "tool_count": 0})
    assert len(calls) == 1
    assert result["tool_count"] == 2
    assert len(result["messages"]) == 2
    assert {m.tool_call_id for m in result["messages"]} == {"one", "two"}
    assert result["messages"][0].content == result["messages"][1].content
