import json
from datetime import datetime,timezone
from pathlib import Path
from uuid import uuid4

LOG = Path(__file__).resolve().parents[2] / 'logs' / 'events.jsonl'

def new_run_id(): return uuid4().hex

def record_event(run_id,event,**fields):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    # Do not log raw prompts, tool arguments, API secrets or full document passages.
    item = {'timestamp':datetime.now(timezone.utc).isoformat(),'run_id':run_id,'event':event,**fields}
    with LOG.open('a',encoding='utf-8') as f: f.write(json.dumps(item,ensure_ascii=False)+'\n')
