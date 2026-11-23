"""Conservative demo guardrails: not a complete prompt-injection defense."""
import re

def check_input(query: str):
    if not isinstance(query,str) or not query.strip(): return 'Vui lòng nhập câu hỏi.'
    if len(query)>1000: return 'Câu hỏi quá dài (tối đa 1000 ký tự).'
    if re.search(r'(?i)(drop\s+table|delete\s+from|rm\s+-rf|ignore\s+(all\s+)?previous\s+instructions)',query):
        return 'Yêu cầu có nội dung không được phép trong bản demo.'
    return None

def check_tool(name, args):
    """Allow only read-only named tools with type-checked, bounded arguments."""
    if name not in {'search_books', 'check_availability', 'search_library_policy'}:
        return 'Công cụ không được cho phép.'
    if not isinstance(args, dict):
        return 'Tham số công cụ không hợp lệ.'
    allowed = {
        'search_books': {'query', 'limit'},
        'check_availability': {'book_id'},
        'search_library_policy': {'query', 'k'},
    }
    if set(args) - allowed[name]:
        return 'Tham số ngoài danh sách cho phép.'
    if name in ('search_books', 'search_library_policy'):
        query = args.get('query')
        if not isinstance(query, str) or not query.strip() or len(query) > 200:
            return 'Từ khóa phải là chuỗi 1–200 ký tự.'
        optional = 'limit' if name == 'search_books' else 'k'
        if optional in args:
            v = args[optional]
            bound = 10 if name == 'search_books' else 5
            if type(v) is not int or not 1 <= v <= bound:
                return f'{optional} phải là số nguyên từ 1 đến {bound}.'
    else:
        book_id = args.get('book_id')
        if type(book_id) is not int or not 1 <= book_id <= 1_000_000:
            return 'book_id phải là số nguyên hợp lệ.'
    return None


def check_output(content):
    """Extract text from Gemini/LangChain content blocks; do not expose signatures."""
    if isinstance(content,str): text=content
    elif isinstance(content,list):
        parts=[]
        for block in content:
            if isinstance(block,str):parts.append(block)
            elif isinstance(block,dict) and block.get('type')=='text' and isinstance(block.get('text'),str):
                parts.append(block['text'])
        text='\n'.join(parts)
    else:text=''
    return text.strip() or 'Không tạo được câu trả lời hợp lệ.'
