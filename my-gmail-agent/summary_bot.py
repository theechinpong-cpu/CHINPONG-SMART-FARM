import os
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_gmail_summary():
    # 1. ตั้งค่า Gmail API ด้วย Refresh Token จาก Secrets
    creds = Credentials.from_authorized_user_info({
        "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
        "client_id": os.getenv("GMAIL_CLIENT_ID"),
        "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
        "token_uri": "https://oauth2.googleapis.com/token",
    })
    
    service = build('gmail', 'v1', credentials=creds)
    
    # 2. ดึงรายการอีเมลล่าสุด (15 ฉบับล่าสุด)
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])
    
    full_text = ""
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        full_text += f"- {m['snippet']}\n"

    # 3. ใช้ Gemini สรุปข้อมูล
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"คุณคือเลขาส่วนตัว สรุปอีเมลต่อไปนี้เป็นภาษาไทย แยกเป็นหัวข้อที่สำคัญและต้องจัดการด่วน:\n{full_text}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    try:
        result = get_gmail_summary()
        print(f"=== สรุปอีเมลประจำรอบเวลา ===\n{result}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
