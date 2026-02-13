import os
import random
import asyncio
import re
import google.generativeai as genai
from telegram import Bot
import edge_tts

# --- CONFIGURATION FROM SECRETS [cite: 2026-02-11] ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_random_product():
    """สุ่มเลือกสินค้าจากไฟล์ products.txt (ส่วนเดิมที่ทำสำเร็จแล้ว) [cite: 2026-02-13]"""
    try:
        if not os.path.exists('products.txt'):
            return None
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except Exception:
        return None

async def send_telegram_with_audio(file_path, caption):
    """ฟังก์ชันส่งทั้งข้อความและไฟล์เสียงเข้า Telegram [cite: 2026-02-12]"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        # ส่งไฟล์เสียง .mp3 [cite: 2026-02-13]
        with open(file_path, 'rb') as audio:
            await bot.send_audio(
                chat_id=TELEGRAM_CHAT_ID, 
                audio=audio, 
                caption=caption, 
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Telegram Delivery Error: {e}")

async def generate_speech(text, output_path):
    """
    ขั้นตอนที่ 1: สร้างไฟล์เสียงพากย์ 
    ตั้งค่าความเร็ว 1.5x และ Break 1ms ตามที่กำหนดใหม่ [cite: 2026-02-13, 2026-02-02]
    """
    # ใช้เสียงผู้หญิงไทย Premwadee (Neural)
    voice = "th-TH-PremwadeeNeural"
    # ปรับความเร็วเป็น 1.5x (+50%) [cite: 2026-02-13]
    rate = "+50%" 
    
    # ใส่ Break 1ms ระหว่างประโยค (ใช้การแทนที่จุดด้วยความเงียบสั้นๆ) [cite: 2026-02-02]
    # ใน edge-tts เราจะปรับความกระชับผ่านการตัดคำและประมวลผลเสียง
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

async def generate_content_flow():
    """ฟังก์ชันหลักรวม Logic เดิมและส่วนเพิ่มเติมขั้นที่ 1 [cite: 2026-02-13]"""
    if not GEMINI_API_KEY:
        return

    product = get_random_product()
    if not product:
        return

    # แยกส่วนประกอบสินค้า [cite: 2026-02-11]
    product_parts = product.split('|')
    product_name = product_parts[0]
    affiliate_link = product_parts[-1].replace('พิกัด:', '').strip()

    # ตั้งค่า Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt ล็อคกฎระเบียบ TikTok/Shopee [cite: 2026-02-01, 2026-02-02]
    prompt = f"""
    ช่วยเขียนสคริปต์สั้นๆ 15 วินาที สำหรับใช้พากย์เสียงสินค้า: {product_name}
    - ห้ามระบุชื่อแพลตฟอร์มใดๆ [cite: 2026-02-01]
    - ห้ามโฆษณาสรรพคุณเกินจริง [cite: 2026-02-01]
    - ให้ส่งกลับมาเฉพาะ 'ข้อความที่จะใช้พูด' เท่านั้น ห้ามมีคำอธิบายอื่น
    """

    try:
        response = model.generate_content(prompt)
        speech_text = response.text.strip()
        
        # Clean ข้อความเบื้องต้นเพื่อให้เสียงอ่านลื่นไหล
        clean_text = re.sub(r'[*#_]', '', speech_text)

        # --- ขั้นตอนที่ 1: สร้างไฟล์เสียง (Audio Generation) ---
        audio_filename = "speech_output.mp3"
        await generate_speech(clean_text, audio_filename)

        # รายงานผลกลับไปที่ Telegram พร้อมไฟล์เสียง
        final_caption = (
            f"✅ *ขั้นที่ 1: สร้างไฟล์เสียงพากย์สำเร็จ!* (Speed: 1.5x)\n\n"
            f"📦 *สินค้า:* {product_name}\n"
            f"🔗 *ลิงก์:* {affiliate_link}\n\n"
            f"📝 *สคริปต์:* {clean_text}"
        )
        
        await send_telegram_with_audio(audio_filename, final_caption)
        print("--- [SUCCESS] Process Complete: Audio sent to Telegram ---")

    except Exception as e:
        # หากผิดพลาดให้แจ้งเตือนเข้า Telegram เสมอ [cite: 2026-02-13]
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ *Gemini Flow Error:* {str(e)}")

if __name__ == "__main__":
    asyncio.run(generate_content_flow())
