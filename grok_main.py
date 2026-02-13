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
        requests.post(url, json={"chat_id": chat_id, "text": f"🤖 <b>Grok Diagnostic:</b>\n{msg}", "parse_mode": "HTML"})

def generate_content():
    api_key = os.getenv("GROK_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # 1. ค้นหาโมเดลที่ Key นี้ใช้ได้จริง (Dynamic Discovery) [cite: 2026-02-11]
    try:
        model_list = client.models.list()
        available_models = [m.id for m in model_list.data]
        if not available_models:
            send_telegram("❌ Key นี้ไม่สามารถเข้าถึงโมเดลใดๆ ได้เลย")
            return
        
        # เลือกโมเดลตัวแรกที่ระบบอนุญาต [cite: 2026-02-11]
        active_model = available_models[0] 
        print(f"Available models: {available_models}")
    except Exception as e:
        send_telegram(f"❌ ไม่สามารถดึงรายชื่อ Model ได้: {str(e)}")
        return

    # 2. ดึงข้อมูลสินค้า
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            product = random.choice([l.strip() for l in f if l.strip()])
    except Exception:
        send_telegram("❌ ไม่พบไฟล์ products.txt")
        return

    # 3. รัน Content Generation [cite: 2026-02-01, 2026-02-02]
    try:
        completion = client.chat.completions.create(
            model=active_model,
            messages=[
                {"role": "system", "content": "Expert TikTok 9:16 Creator. No platform names. [cite: 2026-02-01]"},
                {"role": "user", "content": f"สร้างสคริปต์ 9:16 4k ultra realistic: {product} [cite: 2026-02-02]"}
            ]
        )
        
        result = completion.choices[0].message.content
        send_telegram(f"✅ <b>สำเร็จด้วยรุ่น: {active_model}</b>\n\n{result}")
        
    except Exception as e:
        # หากพัง ส่งรายชื่อรุ่นทั้งหมดที่มีให้เลือกใน Telegram
        models_str = ", ".join(available_models)
        send_telegram(f"❌ <b>Error with {active_model}:</b>\n{str(e)}\n\n<b>Models you can use:</b>\n{models_str}")

if __name__ == "__main__":
    generate_content()
