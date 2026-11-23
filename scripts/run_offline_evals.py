"""Offline evaluations; never contacts Gemini. Run: python -m scripts.run_offline_evals"""
from __future__ import annotations
import argparse,json,sys,datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=ROOT/'evals'/'cases.json'
REPORT=ROOT/'reports'/'offline_evals.json'

def run_cases(cases:list[dict])->dict:
    from scripts.init_db import init_database
    from src.tools.library_tools import search_books,check_availability
    from src.guardrails.rules import check_input
    from src.rag.engine import retrieve, INDEX_PATH
    init_database()
    results=[]
    for case in cases:
        kind=case['kind'];row={'id':case['id'],'kind':kind,'status':'error','reason':''}
        try:
            if kind=='catalog':
                payload=json.loads(search_books.invoke({'query':case['query'],'limit':10}))
                found=any(case['expected_title'].casefold() in x['title'].casefold() for x in payload['books'])
            elif kind=='stock':
                payload=json.loads(check_availability.invoke({'book_id':case['book_id']}))
                found=payload['book'] is not None and payload['book']['available_copies']==case['expected_available']
            elif kind=='guardrail':found=bool(check_input(case['query']))==case['expected_block']
            elif kind=='policy':
                if not INDEX_PATH.exists():
                    row.update(status='skipped',reason='RAG index missing; run python -m scripts.build_rag_index')
                    results.append(row);continue
                payload=retrieve(case['query'],k=3)
                found=any(x['section']==case['expected_section'] for x in payload['passages'])
            else:
                row.update(reason='unknown case type');results.append(row);continue
            row.update(status='passed' if found else 'failed',reason='' if found else 'expected value not found')
        except Exception as exc:
            row.update(status='error',reason=f'{type(exc).__name__}: {str(exc)[:160]}')
        results.append(row)
    counts={status:sum(r['status']==status for r in results) for status in ('passed','failed','error','skipped')}
    executed=counts['passed']+counts['failed']+counts['error']
    return {'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope':'OFFLINE ONLY: catalog/stock/semantic RAG/input guardrails; no Gemini or end-to-end answer evaluation',
            'total_cases':len(results),'executed':executed,'pass_rate':round(counts['passed']/executed,3) if executed else None,
            'counts':counts,'results':results}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(REPORT));parser.add_argument('--strict',action='store_true',help='fail if any case failed, errored or skipped')
    args=parser.parse_args()
    cases=json.loads(CASES.read_text(encoding='utf-8'))
    report=run_cases(cases)
    dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('OFFLINE EVALS:',report['counts'],'executed:',report['executed'],'pass_rate:',report['pass_rate'])
    print('Report:',dest)
    for row in report['results']:
        if row['status']!='passed': print(row['id'],row['status'],row['reason'])
    if report['counts']['failed'] or report['counts']['error'] or (args.strict and report['counts']['skipped']):sys.exit(1)

if __name__=='__main__':main()
