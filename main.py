import os
import requests
import google.generativeai as genai
from google.api_core import exceptions

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_and_send():
    genai.configure(api_key=GEMINI_KEY)
    
    # เรียงลำดับจากคุณภาพสูงสุดลงมา (Best -> Good -> Fast)
    models_to_try = [
        'gemini-2.0-flash',        # อันดับ 1: ฉลาดและครบเครื่องที่สุด
        'gemini-2.0-flash-lite',   # อันดับ 2: เร็วและแม่นยำ (ประหยัด Quota)
        'gemini-1.5-flash',        # อันดับ 3: รุ่นมาตรฐานที่เสถียรมาก
        'gemini-1.5-flash-lite',   # อันดับ 4: รุ่นประหยัดสำหรับงานทั่วไป
        'gemma-3-12b-it'           # อันดับ 5: รุ่นเล็กเน้นความไวสูงสุด
    ]
    
    content = None
    used_model = ""

    for model_name in models_to_try:
        try:
            print(f"กำลังลองใช้: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            # คำสั่งสร้างเนื้อหาตามสไตล์ที่คุณต้องการ [cite: 2026-02-11]
            prompt = """
            เขียนสคริปต์วิดีโอ TikTok 9:16 สินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น' 
            ของ ChinPong Smart Farm เน้นความน่าตื่นเต้น ประโยชน์ และการใช้งานที่ง่าย
            """
            
            response = model.generate_content(prompt)
            if response and response.text:
                content = response.text
                used_model = model_name
                break # เจอตัวที่ใช้ได้แล้ว หยุดทันที
                
        except (exceptions.ResourceExhausted, exceptions.InvalidArgument, Exception) as e:
            # ถ้าติดลิมิต หรือรุ่นนั้นไม่รองรับ ให้ขยับไปตัวถัดไป
            print(f"รุ่น {model_name} ใช้ไม่ได้เนื่องจาก: {str(e)}")
            continue

    # ส่งผลลัพธ์เข้า Telegram
    if content:
        message = f"🎬 **สคริปต์วิดีโอพร้อมแล้ว!**\n\n(สร้างโดย: {used_model})\n\n---\n\n{content}"
    else:
        message = "❌ **Error:** ไม่สามารถใช้งาน AI ได้ทุกเวอร์ชันในขณะนี้ เนื่องจากติดลิมิตทั้งหมด"

    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    generate_and_send()
