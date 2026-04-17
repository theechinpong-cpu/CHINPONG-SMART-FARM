import os
import random
import requests

def send_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    
    # 1. Dynamic Model Discovery - ป้องกัน Error 404 ถาวร [cite: 2026-02-11]
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_data = requests.get(list_url).json()
        available = [m['name'] for m in models_data.get('models', []) 
                     if 'flash' in m['name'].lower() and 'generateContent' in m['supportedGenerationMethods']]
        active_model = available[0] if available else "models/gemini-1.5-flash"
    except:
        active_model = "models/gemini-1.5-flash"

    # 2. เลือกสินค้าจากลิสต์
    product = "สินค้าขายดี"
    if os.path.exists('products.txt'):
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
            if lines: product = random.choice(lines)

    # 3. สั่ง Gen สคริปต์วิดีโอ TikTok 9:16 แบบเอาไปใช้ได้เลย [cite: 2026-02-02]
    prompt = (
        f"สร้างสคริปต์วิดีโอ TikTok 9:16 สำหรับสินค้า: {product}\n"
        "โครงสร้าง: 1. Hook ดึงดูด 2. ปัญหา 3. ทางออก(สินค้า) 4. Call to action\n"
        "ห้ามมีชื่อแพลตฟอร์ม [cite: 2026-02-01]\n"
        "บอกรายละเอียด Visual: (ฉากที่ต้องเห็น) และ Audio: (เสียงพูด)"
    )

    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(gen_url, json=payload, timeout=30)
        data = response.json()
        
        if 'candidates' in data:
            content = data['candidates'][0]['content']['parts'][0]['text']
            # ส่งเข้า Telegram ทันที
            send_telegram(f"🎬 <b>สคริปต์วิดีโอสำหรับ: {product}</b>\n\n{content}")
        else:
            send_telegram(f"❌ API Error: {str(data.get('error', {}).get('message', data))}")
    except Exception as e:
        send_telegram(f"❌ System Failure: {str(e)}")

if __name__ == "__main__":
    main()
