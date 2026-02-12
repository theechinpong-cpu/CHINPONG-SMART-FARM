import os
import requests
import google.generativeai as genai
from gtts import gTTS
import subprocess
from google.api_core import exceptions

# ตั้งค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_video_automation():
    genai.configure(api_key=GEMINI_KEY)
    
    # ลำดับ Model ที่คุณมีสิทธิ์ใช้จริง (เรียงจากฉลาดสุดไปหาน้อยสุด)
    models_to_try = [
        'gemini-2.0-flash', 
        'gemini-1.5-flash',
        'gemini-2.0-flash-lite-001',
        'gemma-3-12b-it'
    ]
    
    script_content = None
    used_model = ""

    # --- 1. Generate Script & Caption (พร้อมระบบ Failover) ---
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # สั่งให้เจนสคริปต์ตามสไตล์ที่กำหนด (Vertical 9:16, 4k realistic vibe)
            prompt = """
            เขียนสคริปต์สั้น TikTok 9:16 สำหรับ 'เครื่องสกัดสมุนไพรสกัดเย็น' ChinPong Smart Farm 
            เน้นความเร็ว ความเป็นมืออาชีพ พร้อมแคปชั่นที่มีแฮชแท็กและที่ว่างสำหรับลิงก์สินค้า
            """
            response = model.generate_content(prompt)
            if response and response.text:
                script_content = response.text
                used_model = model_name
                break
        except (exceptions.ResourceExhausted, exceptions.InvalidArgument, Exception):
            continue

    if not script_content:
        # หากติดลิมิตทุกตัว แจ้งเตือนเข้า Telegram
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": "❌ ติดลิมิตทุก Model โปรดรอสักครู่แล้วค่อยเทสใหม่ครับ"})
        return

    try:
        # --- 2. Generate Voice (Speed 2.9x ตามคำสั่ง) ---
        # หมายเหตุ: gTTS พื้นฐานปรับ speed ได้แค่ช้า/เร็ว แต่เราจะใช้ FFmpeg เร่งความเร็วเพิ่มในขั้นตอนถัดไป
        tts_text = script_content.split('\n')[0][:150] # ดึงใจความสำคัญมาทำเสียง
        tts = gTTS(text=tts_text, lang='th')
        tts.save("raw_voice.mp3")

        # --- 3. Render Video ด้วย FFmpeg (9:16 Vertical) ---
        # ขั้นตอนนี้จะรวมการเร่งเสียงเป็น 2.9x และสร้างวิดีโอ 4K Ultra Realistic (Placeholder)
        subprocess.run([
            'ffmpeg', '-y', 
            '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=10', # สร้างพื้นหลังแนวตั้ง 1080x1920
            '-i', 'raw_voice.mp3',
            '-filter_complex', "[1:a]atempo=2.9[a]", # เร่งความเร็วเสียงเป็น 2.9x
            '-map', '0:v', '-map', '[a]',
            '-c:v', 'libx264', '-preset', 'ultrafast', '-shortest', 'output_video.mp4'
        ])

        # --- 4. ส่ง Video เข้า Telegram ---
        with open("output_video.mp4", "rb") as video:
            requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendVideo", 
                          data={"chat_id": CHAT_ID}, files={"video": video})

        # --- 5. ส่ง Caption และลิงก์สินค้า ---
        product_link = "https://shopee.co.th/chinpong_smart_farm" # ลิงก์ร้านของคุณ
        final_message = f"🎬 **Video Ready! (Created by: {used_model})**\n\n{script_content}\n\n📍 **สั่งซื้อที่นี่:** {product_link}"
        
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": final_message, "parse_mode": "Markdown"})

    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": f"❌ Error ระหว่าง Render: {str(e)}"})

if __name__ == "__main__":
    generate_video_automation()
