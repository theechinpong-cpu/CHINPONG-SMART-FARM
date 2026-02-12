import os
import requests
import google.generativeai as genai
from gtts import gTTS
import subprocess

# ดึงค่าจาก Secrets
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def generate_video_automation():
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # 1. สร้างเนื้อหา (สคริปต์ และ แคปชั่น)
        prompt = """
        เขียนสคริปต์สั้นสำหรับ TikTok (ไม่เกิน 15 วินาที) สินค้า 'เครื่องสกัดสมุนไพรสกัดเย็น'
        พร้อมแคปชั่นที่น่าดึงดูด แฮชแท็กที่เกี่ยวข้อง และเว้นวรรคให้ใส่ลิงก์สินค้า
        """
        response = model.generate_content(prompt)
        full_text = response.text

        # 2. สร้างเสียงบรรยาย (TTS)
        tts = gTTS(text=full_text[:100], lang='th') # เอาส่วนหนึ่งของสคริปต์มาทำเสียง
        tts.save("voice.mp3")

        # 3. สร้างภาพประกอบ (ในที่นี้เราจะใช้ภาพสีพื้นหรือภาพตัวอย่างไปก่อน เพราะ API รูปภาพส่ง URL ตรงไม่ได้)
        # หมายเหตุ: ขั้นตอนนี้ใน GitHub Actions ปกติจะใช้ภาพที่เราเตรียมไว้ใน Repo หรือเจนใหม่
        # เพื่อความชัวร์ ผมจะใช้ FFmpeg สร้างวิดีโอจากภาพนิ่งสีพื้นที่มีข้อความประกอบ
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=720x1280:d=5', 
            '-vf', f"drawtext=text='Smart Farm Herb Extractor':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
            '-i', 'voice.mp3', '-shortest', '-c:v', 'libx264', '-c:a', 'aac', 'output_video.mp4'
        ])

        # 4. ส่งวิดีโอเข้า Telegram
        url_video = f"https://api.telegram.org/bot{TELE_TOKEN}/sendVideo"
        with open("output_video.mp4", "rb") as video:
            requests.post(url_video, data={"chat_id": CHAT_ID}, files={"video": video})

        # 5. ส่งแคปชั่นและลิงก์สินค้า (คุณสามารถแก้ลิงก์เป็นของ Shopee/TikTok คุณได้เลย)
        product_link = "https://shopee.co.th/your-product-link" # <-- แก้เป็นลิงก์ของคุณ
        caption = f"🎬 **วิดีโอของคุณพร้อมแล้ว!**\n\n{full_text}\n\n📍 **พิกัดสินค้า:** {product_link}"
        
        url_msg = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": caption, "parse_mode": "Markdown"})

    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    generate_video_automation()
