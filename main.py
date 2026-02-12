import os
import requests
import google.generativeai as genai

# Setup API Keys จาก GitHub Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    try:
        # 1. สร้างเนื้อหาด้วย Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = "เขียนสคริปต์วิดีโอ TikTok 9:16 สินค้า 'เครื่องสกัดสมุนไพร' เน้นความรู้ ห้ามโอ้อวดเกินจริง"
        response = model.generate_content(prompt)
        content = response.text if response.text else "Gemini ไม่สามารถสร้างเนื้อหาได้"

        # 2. ส่งเข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🚀 **สคริปต์ใหม่พร้อมให้ตรวจสอบ:**\n\n{content}",
            "reply_markup": {
                "inline_keyboard": [[
                    {"text": "✅ อนุมัติและโพสต์", "callback_data": "approve"},
                    {"text": "❌ แก้ไขใหม่", "callback_data": "retry"}
                ]]
            },
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
        print("Success: Content sent to Telegram")

    except Exception as e:
        # ถ้าพัง ให้ส่ง Error ไปบอกใน Telegram จะได้รู้จุดแก้
        error_msg = f"❌ **System Error:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_msg})
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_and_send()
