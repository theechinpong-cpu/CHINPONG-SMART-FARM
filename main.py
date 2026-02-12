import os
import requests
import google.generativeai as genai

# ดึงค่าจาก Secrets (ที่เราตั้งค่าไว้ในหน้า GitHub)
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    try:
        # 1. ตั้งค่าและสั่ง Gemini เจนคอนเทนต์
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "เขียนสคริปต์ TikTok 9:16 สินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น' สำหรับ Smart Farm ให้ดูน่าสนใจและเป็นมืออาชีพ"
        response = model.generate_content(prompt)
        
        # 2. ตรวจสอบเนื้อหา
        if response and response.text:
            content = response.text
        else:
            content = "ขออภัยครับ AI ไม่สามารถสร้างเนื้อหาได้ในขณะนี้"

        # 3. ส่งผลลัพธ์เข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🎬 **สคริปต์วิดีโอมาแล้วครับ!**\n\n{content}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

    except Exception as e:
        # หากเกิด Error ให้แจ้งเตือนเข้า Telegram ตรงๆ เลยจะได้รู้จุดแก้
        error_info = f"❌ **เกิดข้อผิดพลาด:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_info})

if __name__ == "__main__":
    generate_and_send()
