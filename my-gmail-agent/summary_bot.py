import os
import requests
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message})
        except Exception as e:
            print(f"ส่ง Telegram ไม่สำเร็จ: {e}")

def get_gmail_summary():
    # ดึงค่าจาก Environment Variables ที่ตั้งไว้ใน Workflow
    creds_dict = {
        "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
        "client_id": os.getenv("GMAIL_CLIENT_ID"),
        "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    # ตรวจสอบว่ามีค่าครบไหม
    if not all(creds_dict.values()):
        raise ValueError("ค่า Secrets (ID, Secret หรือ Token) ไม่ครบถ้วน กรุณาตรวจสอบใน GitHub")

    creds = Credentials.from_authorized_user_info(creds_dict)
    service = build('gmail', 'v1', credentials=creds)
    
    # ดึงอีเมล 15 ฉบับล่าสุด
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "ไม่มีอีเมลใหม่ในช่วงนี้ครับ"

    full_text = ""
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        full_text += f"- {m['snippet']}\n"

    # ใช้ Gemini สรุป
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("ไม่พบ GEMINI_API_KEY")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"คุณคือเลขาส่วนตัว สรุปอีเมลต่อไปนี้เป็นภาษาไทย แยกเป็นหัวข้อที่สำคัญและต้องจัดการด่วน:\n{full_text}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    try:
        summary = get_gmail_summary()
        print(summary)
        send_telegram(f"📢 สรุปอีเมลประจำรอบเวลา:\n\n{summary}")
    except Exception as e:
        error_msg = f"❌ ระบบขัดข้อง: {str(e)}"
        print(error_msg)
        send_telegram(error_msg)
