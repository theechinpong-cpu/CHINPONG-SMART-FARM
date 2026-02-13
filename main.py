import os
import random
import requests
import json

# --- ส่วนเดิมที่สำเร็จแล้ว: ฟังก์ชันส่ง Telegram (เพิ่มระบบปุ่ม Inline Keyboard) ---
def send_telegram_with_approval(msg, product_name):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not (token and chat_id): return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # เพิ่มปุ่มเพื่อให้คุณกดอนุมัติหรือปฏิเสธได้ทันทีจาก Telegram [cite: 2026-02-13]
    reply_markup = {
        "inline_keyboard": [[
            {"text": "✅ อนุมัติและสร้างวิดีโอ", "callback_data": f"approve_{product_name}"},
            {"text": "❌ ปฏิเสธ", "callback_data": "reject"}
        ]]
    }

    payload = {
        "chat_id": chat_id,
        "text": f"🔔 <b>[รออนุมัติ]:</b>\n{msg}",
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup),
        "disable_notification": False # Alarm แจ้งเตือนดังแน่นอน
    }
    requests.post(url, json=payload)

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    
    # --- [Verify แล้ว] ส่วนเดิม: Dynamic Model Discovery ---
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(list_url).json()
        active_model = [m['name'] for m in res.get('models', []) if 'flash' in m['name'].lower()][0]
    except:
        active_model = "models/gemini-1.5-flash"

    # --- [Verify แล้ว] ส่วนเดิม: Product Selection ---
    product = "สินค้าเกษตรอัจฉริยะ"
    if os.path.exists('products.txt'):
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
            if lines: product = random.choice(lines)

    # --- ส่วนเดิมที่สำเร็จแล้ว: การ Gen สคริปต์ (ปรับปรุงเพื่อการส่งอนุมัติ) ---
    prompt = (
        f"สร้างสคริปต์วิดีโอ TikTok 9:16 สำหรับ: {product} (เน้นขายของคอมมิชชั่นสูง)\n"
        "สรุป Hook, เนื้อหา และ Call to Action ให้ชัดเจน"
    )

    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={api_key}"
    
    try:
        response = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
        content = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # ส่งข้อมูลให้คุณอนุมัติผ่าน Telegram พร้อมปุ่มกด [cite: 2026-02-13]
        send_telegram_with_approval(f"สคริปต์สำหรับ {product}:\n\n{content}", product)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
