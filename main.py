import os
import requests
import google.generativeai as genai
from gtts import gTTS
import subprocess
from google.api_core import exceptions

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_video_automation():
    genai.configure(api_key=GEMINI_KEY)
    
    # ลำดับความสำคัญของ Model (ถ้าตัวบนติดลิมิต 429 จะขยับลงมาข้างล่าง)
    models_to_try = [
        'gemini-2.0-flash', 
        'gemini-2.0-flash-lite-001', 
        'gemini-1.5-flash', 
        'gemini-1.5-flash-lite'
    ]
    
    script_content = None
    used_model = ""

    # 1. ขั้นตอนสร้างเนื้อหา (พร้อมระบบเช็ค Quota)
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = "เขียนสคริปต์สั้น TikTok 9:16 สินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น' พร้อมแคปชั่นและแฮชแท็ก"
            response = model.generate_content(prompt)
            if response and response.text:
                script_content = response.text
                used_model = model_name
                break
        except exceptions.ResourceExhausted:
            print(f"⚠️ {model_name} ติดลิมิต กำลังลองตัวถัดไป...")
            continue
        except Exception as e:
            continue

    if not script_content:
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": "❌ ติดลิมิตทุก Model โปรดรอสักครู่"})
        return

    try:
        # 2. สร้างเสียงบรรยาย (TTS) - ใช้ส่วนหนึ่งของสคริปต์
        tts_text = script_content.split('\n')[0][:100] # เอาบรรทัดแรกมาทำเสียง
        tts = gTTS(text=tts_text, lang='th')
        tts.save("voice.mp3")

        # 3. Render วิดีโอ (FFmpeg) - สร้างวิดีโอ 9:16 พื้นหลังดำ+ตัวอักษร
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=720x1280:d=5', 
            '-vf', "drawtext=text='Smart Farm Content':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
            '-i', 'voice.mp3', '-shortest', '-c:v', 'libx264', '-c:a', 'aac', 'output_video.mp4'
        ])

        # 4. ส่งวิดีโอเข้า Telegram
        with open("output_video.mp4", "rb") as video:
            requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendVideo", 
                          data={"chat_id": CHAT_ID}, files={"video": video})

        # 5. ส่งแคปชั่นและพิกัดสินค้า (Automated Content)
        product_link = "https://shopee.co.th/your-product-link" # แก้เป็นลิงก์ของคุณ
        final_message = f"🎬 **สร้างโดย: {used_model}**\n\n{script_content}\n\n📍 **พิกัดสินค้า:** {product_link}"
        
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": final_message, "parse_mode": "Markdown"})

    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": f"❌ Render Error: {str(e)}"})

if __name__ == "__main__":
    generate_video_automation()
