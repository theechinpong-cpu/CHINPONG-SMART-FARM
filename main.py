import os
import requests
import google.generativeai as genai

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    try:
        # 1. ตั้งค่า Gemini
        genai.configure(api_key=GEMINI_KEY)
        
        # เปลี่ยนเป็นรุ่น gemini-pro ซึ่งเสถียรที่สุดสำหรับ API ปัจจุบัน
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = "เขียนสคริปต์วิดีโอสั้น 9:16 สินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น' สำหรับ Smart Farm เน้นประโยชน์และการใช้งาน ห้ามโฆษณาเกินจริง"
        
        # 2. เจนเนื้อหา
        response = model.generate_content(prompt)
        
        if response and response.text:
            content = response.text
        else:
            content = "AI ไม่สามารถสร้างเนื้อหาได้ในขณะนี้"

        # 3. ส่งเข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🎬 **สคริปต์วิดีโอพร้อมแล้วครับ!**\n\n{content}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

    except Exception as e:
        # แจ้ง Error ให้ละเอียดขึ้น
        error_info = f"❌ **เกิดข้อผิดพลาด:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_info})

if __name__ == "__main__":
    generate_and_send()
