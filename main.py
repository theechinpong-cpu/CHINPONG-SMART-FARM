import os
import requests
import google.generativeai as genai

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    try:
        # เชื่อมต่อ Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash') # ใช้รุ่น Flash ที่เสถียรและเร็ว
        
        prompt = "เขียนสคริปต์ TikTok 9:16 สินค้า 'เครื่องสกัดสมุนไพร' ให้ดูน่าสนใจ"
        response = model.generate_content(prompt)
        
        # ตรวจสอบว่ามีเนื้อหาตอบกลับมาไหม
        if response and response.text:
            content = response.text
        else:
            content = "AI ไม่สามารถเจนเนื้อหาได้ในขณะนี้"

        # ส่งเข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🚀 **สคริปต์วิดีโอมาแล้วครับ:**\n\n{content}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

    except Exception as e:
        # ถ้าพัง ให้ส่งแจ้งเตือน Error ที่ชัดเจน
        error_msg = f"❌ **System Error:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_msg})

if __name__ == "__main__":
    generate_and_send()
