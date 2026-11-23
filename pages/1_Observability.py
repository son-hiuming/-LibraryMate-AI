"""Local-only dashboard built from sanitized JSONL. No Gemini calls."""
import streamlit as st
import pandas as pd
from src.monitoring.analytics import get_summary
from src.monitoring.logger import LOG

st.set_page_config(page_title='LibraryMate | Observability',page_icon='📈',layout='wide')
st.title('📈 Observability Dashboard')
st.caption('Đọc logs cục bộ; không gọi Gemini hoặc thay đổi dữ liệu. Số lần gọi quan sát được có thể thấp hơn số lần gọi thực tế khi có lỗi.')
if st.button('Làm mới dữ liệu'):
    st.rerun()
s=get_summary()
cols=st.columns(4)
cols[0].metric('Tổng Run ID',s['total_runs'])
cols[1].metric('Runs thành công',s['successful_runs'])
cols[2].metric('Runs lỗi',s['error_runs'])
cols[3].metric('Latency TB (run thành công)',f"{s['mean_success_latency_ms']} ms" if s['mean_success_latency_ms'] is not None else 'N/A')
st.write('**Tỷ lệ thành công trên các lượt đã hoàn tất:**',f"{100*s['success_rate']:.1f}%" if s['success_rate'] is not None else 'Chưa có dữ liệu')
if s['malformed_log_lines']:
    st.warning(f"Có {s['malformed_log_lines']} dòng log không hợp lệ đã bị bỏ qua.")
a,b=st.columns(2)
with a:
    st.subheader('Các công cụ đã gọi')
    if s['tool_calls']:
        st.bar_chart(pd.Series(s['tool_calls'],name='Số lượt'))
    else:st.info('Chưa có tool calls trong logs.')
with b:
    st.subheader('Phân loại lỗi')
    if s['errors']:st.bar_chart(pd.Series(s['errors'],name='Số lượt'))
    else:st.info('Chưa có lỗi được ghi nhận.')
st.subheader('Chi tiết các lượt chạy')
runs=s['runs']
if runs:
    df=pd.DataFrame(runs)
    st.dataframe(df[['run_id','started_at','status','llm_calls_observed','tool_calls_observed','latency_ms','error_type']],use_container_width=True,hide_index=True)
    rid=st.selectbox('Xem timeline của Run ID', [r['run_id'] for r in runs])
    from src.monitoring.analytics import load_events
    events,_=load_events()
    timeline=[{k:v for k,v in e.items() if k not in {'query','prompt','args','content','response'}} for e in events if e['run_id']==rid]
    st.json(timeline)
else:
    st.info(f'Chưa có log tại {LOG}. Hãy chạy ứng dụng và gửi câu hỏi để có dữ liệu.')
st.caption('Không hiển thị câu hỏi hoặc nội dung câu trả lời của người dùng trong dashboard. Logs không phải vết thực thi đầy đủ nếu tiến trình bị dừng đột ngột.')
