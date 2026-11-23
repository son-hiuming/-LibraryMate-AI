"""Viewer of previously generated offline evaluation report (does not run Gemini)."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'reports'/'offline_evals.json'
st.set_page_config(page_title='LibraryMate | Evals',page_icon='🧪',layout='wide')
st.title('🧪 Offline Evaluation Results')
st.caption('Đây là đánh giá offline của SQLite, RAG retrieval và Input Guardrails; KHÔNG phải độ chính xác câu trả lời Gemini.')
if not FILE.exists():
    st.info('Chưa có báo cáo. Mở Terminal và chạy: python -m scripts.run_offline_evals')
else:
    report=json.loads(FILE.read_text(encoding='utf8'))
    c=report['counts'];a,b,d,e=st.columns(4)
    a.metric('Passed',c['passed']);b.metric('Failed',c['failed']);d.metric('Errors',c['error']);e.metric('Skipped',c['skipped'])
    st.write('**Pass rate trên các ca đã thực thi:**',f"{report['pass_rate']*100:.1f}%" if report['pass_rate'] is not None else 'N/A')
    st.caption(f"Generated at: {report.get('generated_at_utc','?')}")
    st.dataframe(pd.DataFrame(report['results']),use_container_width=True,hide_index=True)
    st.download_button('Tải báo cáo JSON',FILE.read_bytes(),file_name='offline_evals.json',mime='application/json')
