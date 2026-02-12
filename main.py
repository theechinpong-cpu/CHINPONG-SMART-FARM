import os
import requests
import json

# ดึงค่าคอนฟิกจาก GitHub Secrets เพื่อความปลอดภัย
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def generate_video_script(product_info):
    """สั่ง Gemini ให้เจนสคริปต์วิดีโอ 9:16 ตามกฎของคุณ [2026-02-01, 2026-02-02]"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Prompt ที่คุมเข้มตามคำสั่งของคุณ
    prompt = (
        f"เขียนสคริปต์วิดีโอแนวตั้ง 9:16 สำหรับสินค้า: {product_info}. "
        "สไตล์: 4k ultra realistic. "
        "ข้อกำหนด: ห้ามระบุชื่อ Platform, ห้ามโฆษณาเกินจริง. "
        "รูปแบบผลลัพธ์: ให้ส่งเฉพาะสคริปต์ในรูปแบบ SSML "
        "โดยตั้งค่า Speed 2.9x และ Break time 1ms เท่านั้น."
    )
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"AI Error: {response.status_code}"

def send_to_approval(script_content):
    """ส่งสคริปต์เข้า Telegram เพื่อรอการอนุมัติ"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # สร้างปุ่มกดอนุมัติสำหรับมือถือ
    reply_markup = {
        "inline_keyboard": [[
            {"text": "✅ อนุมัติและโพสต์", "callback_data": "confirm_post"},
            {"text": "❌ แก้ไขใหม่", "callback_data": "regen"}
        ]]
    }
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚀 **สคริปต์ใหม่พร้อมให้ตรวจสอบ:**\n\n{script_content}",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(reply_markup)
    }
    
    requests.post(url, data=payload)

if __name__ == "__main__":
    # ตัวอย่างสินค้า (ในอนาคตจะเปลี่ยนเป็นดึงจาก Shop API อัตโนมัติ)
    target_product = "เครื่องสกัดสมุนไพรสกัดเย็นเพื่อสุขภาพ"
    
    print(f"🤖 กำลังเจนสคริปต์สำหรับ: {target_product}")
    result = generate_video_script(target_product)
    send_to_approval(result)
    print("✅ ส่งงานเข้า Telegram เรียบร้อยแล้ว")
