import os
import random
import time
import asyncio
import google.generativeai as genai
from telegram import Bot

# --- CONFIGURATION ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID" # ไอดีของคุณที่รับแจ้งเตือน

# ตั้งค่า Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_random_product():
    """สุ่มเลือกสินค้าจากไฟล์ products.txt"""
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except FileNotFoundError:
        print("Error: ไม่พบไฟล์ products.txt")
        return None

async def send_to_telegram(message):
    """ส่งการแจ้งเตือนและ Content เข้า Telegram"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        print("--- [SUCCESS] Notification sent to Telegram ---")
    except Exception as e:
        print(f"--- [ERROR] Telegram Failed: {e} ---")

async def generate_content():
    product = get_random_product()
    if not product:
        print("--- [ERROR] No product found in file ---")
        return

    print(f"--- [SYSTEM] เริ่มทำ Content สำหรับ: {product} ---")
    
    # แยกส่วนประกอบสินค้า
    product_parts = product.split('|')
    product_name = product_parts[0]
    affiliate_link = product_parts[-1].replace('พิกัด:', '').strip()

    # SSML & Content Prompt Optimization [cite: 2026-02-02, 2026-02-01]
    prompt = f"""
    ช่วยสร้างสคริปต์วิดีโอสั้นแนวตั้ง (9:16) สำหรับสินค้า: {product_name}
    Format: TikTok/Reels/Shorts (vertical, 4k ultra realistic)
    เงื่อนไข:
    1. ห้ามมีชื่อแพลตฟอร์มการค้าเด็ดขาด
    2. ห้ามโฆษณาสรรพคุณเกินจริง (ถ้าเป็นสินค้าสุขภาพ)
    3. ความยาว 15 วินาที
    4. สร้างสคริปต์ SSML: speed 2.9x, break time 1ms [cite: 2026-02-02]
    
    ส่งผลลัพธ์ในรูปแบบ:
    [สคริปต์วิดีโอ]
    ...
    [รายละเอียดภาพสำหรับ AI Image Gen]
    ...
    """

    try:
        response = model.generate_content(prompt)
        content_text = response.text

        # สร้างข้อความที่จะส่งเข้า Telegram
        final_report = (
            f"🚀 *New Content Generated!*\n\n"
            f"📦 *สินค้า:* {product_name}\n"
            f"🔗 *พิกัด:* {affiliate_link}\n\n"
            f"📝 *Content Snippet:*\n{content_text[:500]}..." 
        )

        await send_to_telegram(final_report)
        
    except Exception as e:
        error_msg = f"❌ [SYSTEM ERROR]: {str(e)}"
        print(error_msg)
        await send_to_telegram(error_msg)

if __name__ == "__main__":
    # รันแบบ Async เพื่อรองรับ Telegram Bot API
    asyncio.run(generate_content())
