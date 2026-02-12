import os
import random
import requests
import sys

# 1. ตรวจสอบและจัดการ Library แบบไดนามิก
try:
    from openai import OpenAI
    import openai
    OPENAI_V1 = hasattr(openai, 'OpenAI')
except ImportError:
    print("Error: Library 'openai' not found.")
    sys.exit(1)

def get_random_product():
    """ดักจับ Error การอ่านไฟล์สินค้า"""
    try:
        if not os.path.exists('products.txt'):
            return "Error: ไม่พบไฟล์ products.txt"
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        return random.choice(lines) if lines else "Error: ไฟล์สินค้าว่างเปล่า"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def send_telegram_alarm(msg):
    """ระบบ Alarm แจ้งเตือนข้อผิดพลาดเข้า Telegram"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": f"🚨 System Alert:\n{msg}"})

def generate_content():
    # ดึงค่า Config และตรวจสอบความพร้อม
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        send_telegram_alarm("Missing GROK_API_KEY in Secrets")
        return

    product_data = get_random_product()
    if "Error" in product_data:
        send_telegram_alarm(product_data)
        return

    # รายชื่อ Model ที่จะลองใช้ตามลำดับความสำคัญ (Fallback System)
    models_to_try = ["grok-4-latest", "grok-2-latest", "grok-beta"]
    
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    success = False
    last_error = ""

    for model_name in models_to_try:
        try:
            print(f"Attempting with model: {model_name}...")
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Expert TikTok 9:16 Creator. No platform names. [cite: 2026-02-01]"},
                    {"role": "user", "content": f"สร้างสคริปต์ 9:16 4k ultra realistic สำหรับ: {product_data} [cite: 2026-02-02]"}
                ],
                temperature=0,
                timeout=30 # ดักจับกรณี API ค้าง
            )
            
            content = completion.choices[0].message.content
            send_telegram_alarm(f"✅ Success ({model_name}):\n\n{content}")
            success = True
            break # ถ้าสำเร็จให้หยุด Loop
            
        except Exception as e:
            last_error = f"Model {model_name} failed: {str(e)}"
            print(last_error)
            continue # ถ้าพังให้ไปลอง Model ถัดไป

    if not success:
        send_telegram_alarm(f"❌ All models failed. Last error: {last_error}")

if __name__ == "__main__":
    generate_content()
