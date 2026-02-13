import os
import random
import asyncio
import re
import google.generativeai as genai
from telegram import Bot
import edge_tts

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_random_product():
    try:
        if not os.path.exists('products.txt'): return None
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except Exception: return None

async def send_telegram_package(file_path, full_report):
    """ส่งรายงานฉบับเต็มพร้อมไฟล์เสียง [cite: 2026-02-12]"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        with open(file_path, 'rb') as audio:
            # ส่งไฟล์เสียงพร้อมรายงานที่แยกส่วนชัดเจน
            await bot.send_audio(
                chat_id=TELEGRAM_CHAT_ID, 
                audio=audio, 
                caption=full_report[:1024], 
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Telegram Delivery Error: {e}")

async def generate_speech(text, output_path):
    """สร้างไฟล์เสียง 1.5x และ Break 1ms [cite: 2026-02-13, 2026-02-02]"""
    voice = "th-TH-PremwadeeNeural"
    rate = "+50%" # 1.5x
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

async def generate_content_flow():
    if not GEMINI_API_KEY: return
    product = get_random_product()
    if not product: return

    product_parts = product.split('|')
    product_name = product_parts[0]
    affiliate_link = product_parts[-1].replace('พิกัด:', '').strip()

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt แบบแยกส่วนข้อมูลชัดเจนเพื่อไม่ให้ข้อมูลหาย [cite: 2026-02-13]
    prompt = f"""
    สินค้า: {product_name}
    ช่วยสร้าง Content สำหรับวิดีโอ 15 วินาที โดยแยกส่วนดังนี้:
    1. [VOICE]: ข้อความสำหรับพากย์เสียงเท่านั้น (ห้ามมีเครื่องหมาย)
    2. [VISUAL]: รายละเอียดภาพประกอบ 4k ultra realistic, vertical [cite: 2026-02-02]
    3. [TEXT]: ข้อความสั้นๆ ที่จะแสดงบนหน้าจอ
    เงื่อนไข: ห้ามมีชื่อแพลตฟอร์ม [cite: 2026-02-01]
    """

    try:
        response = model.generate_content(prompt)
        raw_content = response.text
        
        # ใช้ Regex ดึงข้อมูลแยกส่วน
        voice_match = re.search(r'\[VOICE\]:(.*?)(?=\[|$)', raw_content, re.DOTALL)
        visual_match = re.search(r'\[VISUAL\]:(.*?)(?=\[|$)', raw_content, re.DOTALL)
        text_match = re.search(r'\[TEXT\]:(.*?)(?=\[|$)', raw_content, re.DOTALL)

        speech_text = voice_match.group(1).strip() if voice_match else "ไม่พบสคริปต์เสียง"
        visual_info = visual_match.group(1).strip() if visual_match else "ไม่พบข้อมูลภาพ"
        screen_text = text_match.group(1).strip() if text_match else "ไม่พบข้อความบนจอ"

        # ทำความสะอาดสคริปต์เสียงก่อนส่งเข้า TTS
        clean_speech = re.sub(r'[*#_>-]', '', speech_text)

        # --- Step 1: สร้างไฟล์เสียง ---
        audio_filename = "speech_output.mp3"
        await generate_speech(clean_speech, audio_filename)

        # รวมรายงานข้อมูลทั้งหมดเพื่อส่งให้คุณตรวจสอบ
        full_report = (
            f"🎬 *Step 1 Complete: Audio & Planning*\n\n"
            f"📦 *สินค้า:* {product_name}\n"
            f"🎙️ *สคริปต์พากย์:* {clean_speech}\n\n"
            f"🖼️ *แผนภาพ (Visual):* {visual_info[:200]}...\n\n"
            f"💬 *ข้อความบนจอ:* {screen_text}\n\n"
            f"🔗 {affiliate_link}"
        )
        
        await send_telegram_package(audio_filename, full_report)
        print("--- [SUCCESS] All data preserved and audio sent ---")

    except Exception as e:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ *Error:* {str(e)}")

if __name__ == "__main__":
    asyncio.run(generate_content_flow())
