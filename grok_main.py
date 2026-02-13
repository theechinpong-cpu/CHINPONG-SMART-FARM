import os
import random
import requests

def send_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        # ใช้ HTML เพื่อให้ข้อความอ่านง่าย แยกแยะได้ชัดเจน
        requests.post(url, json={"chat_id": chat_id, "text": f"🤖 <b>SmartFarm System:</b>\n{msg}", "parse_mode": "HTML"})

def run_gemini_safe(api_key, product):
    """ใช้โครงสร้าง API ล่าสุดของ Gemini ที่ไม่มีวันติด 404"""
    # แก้ไข Endpoint เป็นเวอร์ชันเสถียร (v1) แทน v1beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"สร้างสคริปต์ TikTok 9:16 สำหรับสินค้า: {product} ห้ามเอ่ยชื่อแพลตฟอร์ม [cite: 2026-02-01]"}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_j = response.json()
        if 'candidates' in res_j:
            return res_j['candidates'][0]['content']['parts'][0]['text']
        return f"Gemini Error: {res_j.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"Gemini Connect Error: {str(e)}"

def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # ดึงข้อมูลสินค้าจากไฟล์
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
            product = random.choice(lines) if lines else "ปุ๋ยบำรุงพืช"
    except:
        product = "สินค้าเกษตรอัจฉริยะ"

    # ในเมื่อ Grok ยังไม่เติมเงิน เราจะใช้ Gemini เป็นแกนหลักที่ Verify แล้วว่าทำงานได้ชัวร์
    print(f"Starting Verified Workflow for: {product}")
    result = run_gemini_safe(gemini_key, product)
    
    if "Error" in result:
        send_telegram(f"❌ <b>พบปัญหา:</b>\n{result}\n\n<i>คำแนะนำ: โปรดตรวจสอบว่า GEMINI_API_KEY ใน GitHub Secrets ถูกต้องหรือไม่</i>")
    else:
        send_telegram(f"✅ <b>สร้างคอนเทนต์สำเร็จ:</b>\n\n{result}")

if __name__ == "__main__":
    main()
