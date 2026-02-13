import os
import random
import requests
from openai import OpenAI

def send_telegram(msg):
    """ส่ง Alarm เข้า Telegram @chinpongsmartfarmbot"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": f"🤖 <b>Grok System:</b>\n{msg}", "parse_mode": "HTML"})

def get_available_model(client):
    """ระบบค้นหาโมเดลที่ใช้งานได้จริงอัตโนมัติ [cite: 2026-02-11]"""
    try:
        models = client.models.list()
        # ค้นหาโมเดลที่มีคำว่า 'grok' และไม่ใช่รุ่นเก่า
        available = [m.id for m in models.data if 'grok' in m.id.lower()]
        return available[0] if available else "grok-2-1212"
    except Exception:
        return "grok-2-1212" # Fallback ตัวที่เสถียรที่สุด

def generate_content():
    api_key = os.getenv("GROK_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # 1. ดึงโมเดลที่ใช้ได้จริงมา 1 ตัว
    active_model = get_available_model(client)
    
    # 2. ดึงข้อมูลสินค้า
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            product = random.choice([l.strip() for l in f if l.strip()])
    except Exception:
        send_telegram("❌ ไม่พบไฟล์ products.txt")
        return

    # 3. สร้างคอนเทนต์ตามเงื่อนไข TikTok 9:16 [cite: 2026-02-01, 2026-02-02]
    try:
        print(f"Using Model: {active_model}")
        completion = client.chat.completions.create(
            model=active_model,
            messages=[
                {"role": "system", "content": "Expert TikTok 9:16. No platform names. [cite: 2026-02-01]"},
                {"role": "user", "content": f"สร้างสคริปต์ 9:16 4k ultra realistic: {product} [cite: 2026-02-02]"}
            ]
        )
        
        content = completion.choices[0].message.content
        send_telegram(f"✅ <b>สำเร็จด้วยรุ่น: {active_model}</b>\n\n{content}")
        
    except Exception as e:
        send_telegram(f"❌ <b>รันไม่สำเร็จ:</b>\nรุ่นที่พยายามใช้: {active_model}\nสาเหตุ: {str(e)}")

if __name__ == "__main__":
    generate_content()
