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
    # ดึงค่าจาก Env ที่ส่งมาจาก YAML (ชื่อฝั่งซ้ายต้องตรงกับ YAML)
    creds_dict = {
        "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
        "client_id": os.getenv("GMAIL_CLIENT_ID"),
        "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    # Check: ถ้าค่าใดค่าหนึ่งว่าง Python จะ Error ทันที
    for k, v in creds_dict.items():
        if not v:
            raise ValueError(f"ค่า Secret '{k}' ว่างเปล่า! เช็คการตั้งค่าใน GitHub")

    creds = Credentials.from_authorized_user_info(creds_dict)
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "ไม่มีอีเมลใหม่"

    snippets = ""
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippets += f"- {m['snippet']}\n"

    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(f"สรุปอีเมลนี้เป็นภาษาไทยสั้นๆ:\n{snippets}")
    return response.text

if __name__ == "__main__":
    try:
        summary = get_gmail_summary()
        send_telegram(f"📧 สรุปอีเมลพี่ธี:\n\n{summary}")
    except Exception as e:
        send_telegram(f"❌ ระบบขัดข้อง: {str(e)}")
