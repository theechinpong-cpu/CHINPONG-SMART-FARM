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
    # ดึงค่า Env ที่แมตช์กับไฟล์ YAML ด้านล่าง
    creds_dict = {
        "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
        "client_id": os.getenv("GMAIL_CLIENT_ID"),
        "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    # Verify: ตรวจสอบว่ามีค่าว่างถูกส่งมาหรือไม่
    for key, value in creds_dict.items():
        if not value:
            raise ValueError(f"Missing Secret: {key} is empty. Check GitHub Secrets.")

    creds = Credentials.from_authorized_user_info(creds_dict)
    service = build('gmail', 'v1', credentials=creds)
    
    # ดึงอีเมลล่าสุด (จำกัด 15 ฉบับ)
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "ไม่มีอีเมลใหม่ในช่วงนี้ครับ"

    full_content = ""
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        full_content += f"- {m['snippet']}\n"

    # Gemini Config
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"คุณคือเลขาส่วนตัว สรุปอีเมลต่อไปนี้เป็นภาษาไทย แยกเป็นหัวข้อสำคัญและสิ่งที่ต้องจัดการด่วน:\n{full_content}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    try:
        summary = get_gmail_summary()
        print(summary)
        send_telegram(f"📢 สรุปอีเมลของพี่ธี:\n\n{summary}")
    except Exception as e:
        error_info = f"❌ ระบบขัดข้อง: {str(e)}"
        print(error_info)
        send_telegram(error_info)
