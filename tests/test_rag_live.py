"""Optional integration test: run after `python -m scripts.build_rag_index`.
Usage: python -m pytest -q tests/test_rag_live.py
"""
from pathlib import Path
import pytest
from src.rag.engine import INDEX_PATH, retrieve

@pytest.mark.skipif(not INDEX_PATH.exists(),reason='Build RAG index first')
def test_vietnamese_paraphrase_renewal():
    result=retrieve('Tôi có thể giữ cuốn sách thêm một tuần được không?',k=3)
    assert result['retrieval']=='semantic_chroma'
    assert any(p['section']=='P03' for p in result['passages'])

@pytest.mark.skipif(not INDEX_PATH.exists(),reason='Build RAG index first')
def test_vietnamese_loan_period():
    result=retrieve('Được phép mang tài liệu về nhà mấy hôm?',k=3)
    assert any(p['section']=='P02' for p in result['passages'])
