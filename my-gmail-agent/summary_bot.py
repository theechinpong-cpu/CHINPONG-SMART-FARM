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
            requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=15)
        except Exception as e:
            print(f"Telegram Error: {e}")

def get_gmail_summary():
    # ดึงค่าจาก Env ให้ตรงกับชื่อในไฟล์ YAML
    creds_dict = {
        "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
        "client_id": os.getenv("GMAIL_CLIENT_ID"),
        "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    # ตรวจสอบว่าไม่มีค่าไหนเป็น None หรือว่างเปล่า
    for k, v in creds_dict.items():
        if not v:
            raise ValueError(f"Secret '{k}' is missing! Check your GitHub Secrets.")

    creds = Credentials.from_authorized_user_info(creds_dict)
    service = build('gmail', 'v1', credentials=creds)
    
    # ดึงอีเมล 15 ฉบับล่าสุด
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "ไม่มีอีเมลใหม่ในช่วงนี้ครับ"

    snippets = ""
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippets += f"- {m['snippet']}\n"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
        
    genai.configure(api_key=api_key)
    
    # เรียก Model โดยใช้ชื่อเต็มเพื่อป้องกัน Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(f"สรุปอีเมลต่อไปนี้เป็นภาษาไทยสั้นๆ แยกประเด็นสำคัญ:\n{snippets}")
        return response.text
    except Exception as e:
        return f"Gemini Error (ลองรันใหม่อีกครั้ง): {str(e)}"

if __name__ == "__main__":
    try:
        summary = get_gmail_summary()
        send_telegram(f"📧 สรุปอีเมลพี่ธี:\n\n{summary}")
    except Exception as e:
        error_info = f"❌ ระบบขัดข้อง: {str(e)}"
        print(error_info)
        send_telegram(error_info)
