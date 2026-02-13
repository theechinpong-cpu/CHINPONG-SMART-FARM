import os
import random
import requests

def send_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        # ใช้ HTML เพื่อให้อ่านสคริปต์ง่ายขึ้น
        requests.post(url, json={"chat_id": chat_id, "text": f"🤖 <b>Verified Bot:</b>\n{msg}", "parse_mode": "HTML"})

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    
    # --- STEP 1: DYNAMIC MODEL DISCOVERY (แก้ปัญหาชื่อรุ่นเปลี่ยน) ---
    try:
        # ถาม Google ว่าตอนนี้คีย์นี้ใช้รุ่นไหนได้บ้าง
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_data = requests.get(list_url).json()
        
        # ค้นหารุ่นที่มีคำว่า 'flash' และรองรับการสร้างเนื้อหา
        available_models = [
            m['name'] for m in models_data.get('models', []) 
            if 'flash' in m['name'].lower() and 'generateContent' in m['supportedGenerationMethods']
        ]
        
        # ถ้าหาเจอ ให้เลือกตัวแรก (ซึ่งมักจะเป็นตัวเสถียรล่าสุด) ถ้าไม่เจอใช้ตัวสำรอง
        active_model = available_models[0] if available_models else "models/gemini-1.5-flash"
    except Exception as e:
        active_model = "models/gemini-1.5-flash"

    # --- STEP 2: PRODUCT SELECTION ---
    product = "สินค้าเกษตรคุณภาพ"
    if os.path.exists('products.txt'):
        try:
            with open('products.txt', 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines: product = random.choice(lines)
        except: pass

    # --- STEP 3: CONTENT GENERATION (ใช้ Endpoint ที่ Verify แล้ว) ---
    # ใช้ f-string เพื่อใส่ชื่อรุ่นที่ค้นหาได้ลงใน URL โดยตรง
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"สร้างสคริปต์ TikTok 9:16 สำหรับสินค้า: {product} [cite: 2026-02-02]"}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "topK": 40
        }
    }

    try:
        response = requests.post(gen_url, json=payload, timeout=30)
        data = response.json()
        
        if 'candidates' in data:
            content = data['candidates'][0]['content']['parts'][0]['text']
            send_telegram(f"✅ <b>รุ่นที่ใช้: {active_model}</b>\n\n{content}")
        else:
            # ถ้า API ตอบกลับมาแต่ไม่มีเนื้อหา (เช่น ติดเรื่องความปลอดภัย)
            error_detail = str(data.get('error', data))[:200]
            send_telegram(f"❌ <b>API Response Error:</b>\n{error_detail}")
            
    except Exception as e:
        send_telegram(f"❌ <b>Connection Error:</b> {str(e)}")

if __name__ == "__main__":
    main()
