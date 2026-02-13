import os
import random
import requests

def main():
    # 1. ตั้งค่าพื้นฐาน (ดึงจาก Secrets)
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # 2. เลือกสินค้า
    product = "สินค้าเกษตรคุณภาพ"
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            product = random.choice([line.strip() for line in f if line.strip()])
    except: pass

    # 3. สั่งงาน Gemini v1 (Stable Endpoint - ป้องกัน Error 404)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"เขียนสคริปต์ TikTok 9:16 สำหรับ: {product}"}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        # ดึงข้อความออกมา
        if 'candidates' in data:
            content = data['candidates'][0]['content']['parts'][0]['text']
            # 4. ส่งเข้า Telegram
            tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(tg_url, json={"chat_id": chat_id, "text": f"✅ <b>SmartFarm Success:</b>\n\n{content}", "parse_mode": "HTML"})
            print("Successfully sent to Telegram")
        else:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          json={"chat_id": chat_id, "text": f"❌ Gemini Error: {data}"})
    except Exception as e:
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    main()
