import os
import streamlit as st
from dotenv import load_dotenv
from src.agent.graph import ask
from scripts.init_db import DB,init_database

load_dotenv()
st.set_page_config(page_title='LibraryMate AI',page_icon='📚')
st.title('📚 LibraryMate AI')
st.caption('Trợ lý thư viện giả lập — LangGraph + SQLite + Chroma RAG + Gemini')
mode=os.getenv('LIBRARYMATE_MODE','demo').lower()
st.info(f'Chế độ: {mode.upper()} | Quy định: RAG ngữ nghĩa (Chroma). Chế độ DEMO không sử dụng LLM thật.')
if not DB.exists():
    n=init_database()
    st.success(f'Đã khởi tạo {n} bản ghi sách giả lập.')
if 'chat' not in st.session_state:st.session_state.chat=[]
for role,msg in st.session_state.chat:
    with st.chat_message(role):st.markdown(msg)
q=st.chat_input('Ví dụ: Tìm sách Python và cho biết thời hạn mượn?')
if q:
    st.session_state.chat.append(('user',q))
    with st.chat_message('user'):st.markdown(q)
    with st.chat_message('assistant'):
        result=ask(q)
        st.markdown(result['answer'])
        st.caption(f"Run ID: {result['run_id']} | LLM steps: {result['steps'] if result['steps'] is not None else 'N/A'} | Tool calls: {result.get('tool_calls') if result.get('tool_calls') is not None else 'N/A'}")
    st.session_state.chat.append(('assistant',result['answer']))
st.sidebar.header('Kiểm thử nhanh')
st.sidebar.write('• Tìm sách Python\n\n• Gia hạn sách thế nào?\n\n• Tìm sách SQL và thời hạn mượn?')
st.sidebar.caption('Dữ liệu, quy định và tình trạng sách đều là giả lập.')
