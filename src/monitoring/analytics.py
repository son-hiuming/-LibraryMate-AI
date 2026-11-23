"""Read-only, standard-library observability summary of sanitized JSONL agent logs.
No API calls, no raw prompts, no provider secrets are read or emitted.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
from src.monitoring.logger import LOG

KNOWN_EVENTS = {'input_rail','agent','tool_call','llm_error','completed','output_rail','budget_reached'}

def load_events(path: Path = LOG, *, max_lines: int = 50000) -> tuple[list[dict],int]:
    path = Path(path)
    if not path.exists():
        return [], 0
    events=[]; malformed=0
    # Keep analysis bounded; file is append-only, but could be corrupted during abrupt termination.
    from collections import deque
    with path.open('r',encoding='utf-8') as f:
        lines=deque(f,maxlen=max_lines)
    for line in lines:
        try:
            e=json.loads(line)
            if not isinstance(e,dict) or not isinstance(e.get('run_id'),str) or not isinstance(e.get('event'),str):
                malformed+=1;continue
            events.append(e)
        except (ValueError,TypeError): malformed+=1
    return events,malformed

def summarize(events:list[dict],malformed:int=0)->dict:
    runs={}
    tool_counts=Counter(); errors=Counter(); durations=[]; llm_events=0
    for e in events:
        rid=e['run_id']
        r=runs.setdefault(rid,{'run_id':rid,'started_at':e.get('timestamp',''), 'last_event':'',
                               'status':'incomplete','llm_calls_observed':0,'tool_calls_observed':0,
                               'tools':[],'latency_ms':None,'error_type':None})
        r['last_event']=e['event']
        if e.get('event')=='agent':
            r['llm_calls_observed']+=1;llm_events+=1
        if e.get('event')=='tool_call':
            r['tool_calls_observed']+=1
            tool=str(e.get('tool','unknown'));tool_counts[tool]+=1;r['tools'].append(tool)
        if e.get('event')=='completed':
            r['status']=e.get('status','unknown')
            r['latency_ms']=e.get('latency_ms')
            r['error_type']=e.get('error_type')
            if r['status']=='error':errors[str(r['error_type'] or 'unknown')]+=1
            if isinstance(r['latency_ms'],(int,float)) and r['status']=='ok':
                durations.append(r['latency_ms'])
    completed=sum(r['status']!='incomplete' for r in runs.values())
    ok=sum(r['status']=='ok' for r in runs.values())
    error=sum(r['status']=='error' for r in runs.values())
    return {'total_runs':len(runs),'completed_runs':completed,'successful_runs':ok,'error_runs':error,
            'success_rate':round(ok/completed,3) if completed else None,
            'mean_success_latency_ms':round(sum(durations)/len(durations)) if durations else None,
            'observed_agent_events':llm_events,'tool_calls':dict(tool_counts),'errors':dict(errors),
            'malformed_log_lines':malformed,
            'runs':sorted(runs.values(),key=lambda r:r['started_at'],reverse=True)}

def get_summary(path:Path=LOG)->dict:
    events,malformed=load_events(path)
    return summarize(events,malformed)
