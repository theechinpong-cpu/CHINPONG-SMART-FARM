import os
import random
import asyncio
import google.generativeai as genai
from telegram import Bot

# --- ดึงค่าจาก GitHub Secrets ---
# ต้องตั้งค่าใน GitHub: Settings > Secrets > Actions
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_random_product():
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except FileNotFoundError:
        return None

async def run_gemini_flow():
    # ตรวจสอบ API Key เบื้องต้น
    if not GEMINI_API_KEY or not TELEGRAM_TOKEN:
        print("❌ Error: Missing API Keys in Environment Variables")
        return

    product = get_random_product()
    if not product:
        return

    # แยกข้อมูลสินค้า
    product_parts = product.split('|')
    product_name = product_parts[0]
    shopee_link = product_parts[-1].replace('พิกัด:', '').strip()

    # ตั้งค่า Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prompt ตามเงื่อนไขที่คุณกำหนด [cite: 2026-02-01, 2026-02-02]
    prompt = f"""
    สร้างสคริปต์วิดีโอ 15 วินาที สำหรับ: {product_name}
    สไตล์: 9:16 vertical, 4k ultra realistic
    เงื่อนไข: ห้ามมีชื่อแพลตฟอร์ม, ห้ามโฆษณาเกินจริง
    SSML config: speed 2.9x, break time 1ms
    """

    try:
        response = model.generate_content(prompt)
        content = response.text

        # ส่งแจ้งเตือนไปที่ Telegram @chinpongsmartfarmbot [cite: 2026-02-12]
        bot = Bot(token=TELEGRAM_TOKEN)
        message = (
            f"✅ *Gemini Generate Success!*\n\n"
            f"📦 *สินค้า:* {product_name}\n"
            f"🔗 *ลิงก์:* {shopee_link}\n\n"
            f"📝 *Content:*\n{content}"
        )
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        print("--- [SUCCESS] Message sent to Telegram ---")

    except Exception as e:
        # หาก Error ให้แจ้งไปที่ Telegram ด้วย จะได้ไม่เงียบหาย
        error_msg = f"❌ *Gemini Flow Error:* {str(e)}"
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=error_msg)
        print(f"--- [ERROR] {e} ---")

if __name__ == "__main__":
    asyncio.run(run_gemini_flow())
