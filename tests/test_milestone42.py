"""No API calls or live RAG needed."""
import json
from pathlib import Path
from src.monitoring.analytics import load_events,summarize
from scripts.run_offline_evals import CASES,run_cases

def test_log_aggregation(tmp_path):
    path=tmp_path/'events.jsonl'
    events=[{'run_id':'a','timestamp':'2026-11-22T00:00:00+00:00','event':'input_rail'},
            {'run_id':'a','event':'agent','latency_ms':10},
            {'run_id':'a','event':'tool_call','tool':'search_books'},
            {'run_id':'a','event':'completed','status':'ok','latency_ms':100},
            {'run_id':'b','event':'completed','status':'error','error_type':'GoogleRateLimitError','latency_ms':20}]
    path.write_text('\n'.join(json.dumps(x) for x in events)+'\nINVALID\n',encoding='utf8')
    loaded,broken=load_events(path)
    s=summarize(loaded,broken)
    assert (s['total_runs'],s['successful_runs'],s['error_runs'])==(2,1,1)
    assert s['tool_calls']=={'search_books':1}
    assert s['malformed_log_lines']==1
    assert s['mean_success_latency_ms']==100

def test_offline_dataset_30_cases():
    data=json.loads(CASES.read_text(encoding='utf8'))
    assert len(data)==30
    assert {k:sum(c['kind']==k for c in data) for k in {'catalog','stock','policy','guardrail'}}=={
        'catalog':10,'stock':5,'policy':10,'guardrail':5}
    assert len(set(c['id'] for c in data))==30

def test_offline_small_subset_no_llm():
    data=json.loads(CASES.read_text(encoding='utf8'))
    subset=[next(c for c in data if c['id']==id) for id in ('C01','S01','G01')]
    r=run_cases(subset)
    assert r['counts']=={'passed':3,'failed':0,'error':0,'skipped':0}
