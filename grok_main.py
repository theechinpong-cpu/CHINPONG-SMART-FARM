import os
import random
import requests
from openai import OpenAI

# เรียกใช้ API Key จาก Secrets ที่คุณตั้งค่าไว้
client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"), 
    base_url="https://api.x.ai/v1",
)

def get_random_product():
    # สุ่มเลือกสินค้าจากไฟล์ที่คุณเตรียมไว้
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except FileNotFoundError:
        return None

def send_telegram(message):
    # ส่งการแจ้งเตือนไปที่ @chinpongsmartfarmbot
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def generate_content():
    product = get_random_product()
    if not product:
        print("ไม่พบข้อมูลสินค้า")
        return

    # แยกข้อมูลสินค้าเพื่อนำไปทำ Content
    product_parts = product.split('|')
    product_name = product_parts[0].strip()
    
    # สร้าง Prompt สำหรับ Grok-4-latest
    prompt = f"สร้างสคริปต์วิดีโอ TikTok 9:16 สำหรับ: {product_name} สไตล์ 4k ultra realistic"
    
    try:
        completion = client.chat.completions.create(
            model="grok-4-latest", # ใช้รุ่นล่าสุดตามที่คุณทดสอบ
            messages=[
                {"role": "system", "content": "คุณคือผู้เชี่ยวชาญการสร้างวิดีโอ TikTok
