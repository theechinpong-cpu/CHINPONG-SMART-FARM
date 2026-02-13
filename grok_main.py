import os
import random
import requests
from openai import OpenAI

def send_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": f"🚀 <b>SmartFarm Bot:</b>\n{msg}", "parse_mode": "HTML"})

def get_product():
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            return random.choice([l.strip() for l in f if l.strip()])
    except: return "ปุ๋ยน้ำหมักชีวภาพ"

def run_with_grok(api_key, product):
    """พยายามรันด้วย Grok ก่อน"""
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        # ใช้ระบบ Discovery เพื่อหา Model ที่มีสิทธิ์ใช้จริง
        models = client.models.list()
        active_model = models.data[0].id
        
        completion = client.chat.completions.create(
            model=active_model,
            messages=[{"role": "user", "content": f"สร้างสคริปต์ 9:16 4k: {product}"}]
        )
        return completion.choices[0].message.content, active_model
    except Exception as e:
        return None, str(e)

def run_with_gemini(api_key, product):
    """ถ้า Grok พัง (เช่น เงินหมด) ให้ใช้ Gemini เป็นแผนสำรอง"""
    try:
        # ใช้ v1 แทน v1beta เพื่อเลี่ยง Error 404
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": f"สร้างสคริปต์ 9:16 4k: {product}"}]}]}
        response = requests.post(url, json=payload)
        res_j = response.json()
        return res_j['candidates'][0]['content']['parts'][0]['text'], "Gemini-1.5-Flash"
    except Exception as e:
        return None, str(e)

def main():
    product = get_product()
    grok_key = os.getenv("GROK_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    # ขั้นที่ 1: ลองรันด้วย Grok
    content, error = run_with_grok(grok_key, product)
    if content:
        send_telegram(f"✅ <b>Grok Success:</b>\n\n{content}")
        return

    # ขั้นที่ 2: ถ้า Grok ติด 403 (ไม่มีเงิน) หรือ Error อื่น ให้สลับไป Gemini
    send_telegram(f"⚠️ <b>Grok Error:</b> {error}\n🔄 <i>กำลังสลับไปใช้ Gemini แผนสำรอง...</i>")
    
    content, error_gem = run_with_gemini(gemini_key, product)
    if content:
        send_telegram(f"✅ <b>Gemini Backup Success:</b>\n\n{content}")
    else:
        send_telegram(f"❌ <b>ทุกระบบล้มเหลว:</b>\nGrok: {error}\nGemini: {error_gem}\n\n<i>กรุณาเช็ค Credit ใน xAI Console หรือ API Key ครับ</i>")

if __name__ == "__main__":
    main()
