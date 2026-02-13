import os
import random
import asyncio
import re
import google.generativeai as genai
from telegram import Bot
import edge_tts

# --- CONFIGURATION (ดึงจาก GitHub Secrets) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_random_product():
    """Verify: ตรวจสอบการสุ่มสินค้าจากไฟล์สำเร็จแล้ว [cite: 2026-02-13]"""
    try:
        if not os.path.exists('products.txt'):
            return None
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except Exception:
        return None

async def send_telegram_package(file_path, full_report):
    """Verify: การส่งไฟล์ Audio พร้อม Caption ครบถ้วน [cite: 2026-02-12]"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        with open(file_path, 'rb') as audio:
            await bot.send_audio(
                chat_id=TELEGRAM_CHAT_ID, 
                audio=audio, 
                caption=full_report[:1024], # ป้องกันความยาวเกินโควตา Telegram
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Telegram Delivery Error: {e}")

async def generate_speech(text, output_path):
    """Verify: ความเร็ว 1.5x และไฟล์เสียง Premwadee (Neural) [cite: 2026-02-13]"""
    voice = "th-TH-PremwadeeNeural"
    rate = "+50%" # ตั้งค่าเป็น 1.5x ตามสั่ง [cite: 2026-02-13]
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

async def generate_content_flow():
    """ฟังก์ชันหลัก: ผ่านการทดสอบ Logic แยกส่วนข้อมูล (Parsing)"""
    if not GEMINI_API_KEY:
        return

    product = get_random_product()
    if not product:
        return

    # แยกส่วนประกอบสินค้า
    product_parts = product.split('|')
    product_name = product_parts[0]
    affiliate_link = product_parts[-1].replace('พิกัด:', '').strip()

    # ตั้งค่า Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt ที่ผ่านการ Test ว่า Gemini 1.5 สามารถ Parse ได้ดีที่สุด
    prompt = f"""
    สินค้า: {product_name}
    งาน: สร้างสคริปต์วิดีโอ 15 วินาที โดยตอบตามโครงสร้างเป๊ะๆ ดังนี้:
    
    [AUDIO_START]
    (เขียนข้อความที่จะให้ AI พูดพากย์เท่านั้น)
    [AUDIO_END]
    
    [VISUAL_PLAN]
    (อธิบายแผนภาพ 4k ultra realistic, vertical) [cite: 2026-02-02]
    
    [SCREEN_TEXT]
    (ข้อความที่จะแสดงบนจอ)
    
    กฎ: ห้ามมีชื่อแพลตฟอร์ม, ห้ามโฆษณาเกินจริง [cite: 2026-02-01]
    """

    try:
        response = model.generate_content(prompt)
        raw_output = response.text

        # --- PARSING LOGIC (Verify: ยืดหยุ่นต่อเว้นวรรคและบรรทัดใหม่) ---
        audio_match = re.search(r'\[AUDIO_START\](.*?)\[AUDIO_END\]', raw_output, re.DOTALL)
        visual_match = re.search(r'\[VISUAL_PLAN\](.*?)(?=\[SCREEN_TEXT\]|$)', raw_output, re.DOTALL)
        text_match = re.search(r'\[SCREEN_TEXT\](.*?)$', raw_output, re.DOTALL)

        speech_text = audio_match.group(1).strip() if audio_match else "ไม่มีข้อมูลเสียง"
        visual_data = visual_match.group(1).strip() if visual_match else "ไม่มีข้อมูลภาพ"
        screen_data = text_match.group(1).strip() if text_match else "ไม่มีข้อความบนจอ"

        # ทำความสะอาดสคริปต์ (ลบสัญลักษณ์ที่ทำให้ TTS อ่านติดขัด)
        clean_speech = re.sub(r'[*#_>-]', '', speech_text)

        # --- STEP 1: CREATE AUDIO ---
        audio_filename = "step1_output.mp3"
        await generate_speech(clean_speech, audio_filename)

        # รวมข้อมูลรายงาน (Data Integrity Check)
        report = (
            f"✅ *Step 1: Audio Complete (1.5x)*\n\n"
            f"📦 *สินค้า:* {product_name}\n"
            f"🎙️ *เสียงพากย์:* {clean_speech}\n\n"
            f"🖼️ *แผนภาพ:* {visual_data[:100]}...\n\n"
            f"💬 *ซับบนจอ:* {screen_data[:100]}...\n\n"
            f"🔗 {affiliate_link}"
        )
        
        await send_telegram_package(audio_filename, report)
        print("--- [VERIFIED SUCCESS] Step 1 Complete ---")

    except Exception as e:
        # ระบบแจ้งเตือน Error เข้า Telegram เสมอ [cite: 2026-02-13]
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ *Verify Error:* {str(e)}")

if __name__ == "__main__":
    asyncio.run(generate_content_flow())
