import os
import requests
import google.generativeai as genai

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    try:
        # 1. ตั้งค่า Gemini ด้วยรุ่นที่ตรวจเจอ (2.0-flash)
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = """
        เขียนสคริปต์วิดีโอ TikTok 9:16 สำหรับสินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น' 
        ของ ChinPong Smart Farm โดยเน้น:
        1. ความสะดวกในการใช้งาน
        2. การรักษาคุณค่าของสมุนไพร
        3. ปิดท้ายด้วยการเชิญชวนให้ติดตาม
        ขอเนื้อหาที่สนุก น่าตื่นเต้น และใช้ภาษาที่เป็นกันเอง
        """
        
        # 2. เจนเนื้อหา
        response = model.generate_content(prompt)
        content = response.text if response.text else "AI ไม่สามารถสร้างเนื้อหาได้"

        # 3. ส่งเข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🎬 **สคริปต์วิดีโอจาก Gemini 2.0 มาแล้วครับ!**\n\n{content}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

    except Exception as e:
        error_msg = f"❌ **Error:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_msg})

if __name__ == "__main__":
    generate_and_send()
