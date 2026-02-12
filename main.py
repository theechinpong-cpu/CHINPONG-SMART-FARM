import os
import requests

# ดึงค่า Config จาก GitHub Secrets เพื่อความปลอดภัย
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def generate_content_with_gemini(product_name):
    """ส่งคำสั่งให้ Gemini เจนสคริปต์ตามกฎของคุณ [2026-02-01, 2026-02-02]"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # คำสั่งที่คุมเข้มตามความต้องการของคุณ
    prompt_text = (
        f"สร้างสคริปต์วิดีโอแนวตั้ง 9:16 สำหรับสินค้า: {product_name}. "
        "สไตล์: 4k ultra realistic. "
        "ข้อกำหนด: ห้ามระบุชื่อ Platform, ห้ามโฆษณาเกินจริง (กฎ TikTok/Shopee). "
        "รูปแบบผลลัพธ์: ส่งเฉพาะสคริปต์ในรูปแบบ SSML โดยตั้งค่า Speed 2.9x และ Break time 1ms เท่านั้น."
    )
    
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    return "Error generating content"

def send_to_telegram_for_approval(content):
    """ส่งงานเข้า Telegram เพื่อให้คุณกดอนุมัติจากมือถือ"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # สร้างปุ่มกดอนุมัติ (Inline Keyboard)
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ อนุมัติและโพสต์", "callback_data": "approve_post"},
            {"text": "❌ แก้ไขใหม่", "callback_data": "retry_gen"}
        ]]
    }
    
    message_text = f"📋 **งานใหม่รอการอนุมัติ:**\n\n{content}"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    # ตัวอย่าง: ในอนาคตส่วนนี้จะดึงมาจากรายชื่อสินค้าในตะกร้าอัตโนมัติ
    sample_product = "เครื่องสกัดสมุนไพรสกัดเย็น"
    
    print(f"กำลังเริ่มกระบวนการสำหรับ: {sample_product}")
    ai_work = generate_content_with_gemini(sample_product)
    send_to_telegram_for_approval(ai_work)
    print("ส่งงานเข้า Telegram เรียบร้อยแล้ว รอการอนุมัติจากคุณ...")
