import os
import requests
import google.generativeai as genai

GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TELE_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def diagnose_system():
    try:
        genai.configure(api_key=GEMINI_KEY)
        
        # ดึงรายชื่อ Model ทั้งหมดที่ใช้ได้
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        model_list_str = "\n".join(available_models)
        message = f"✅ **เชื่อมต่อสำเร็จ!**\n\nนี่คือ Model ที่คุณใช้ได้:\n{model_list_str}"

        # ส่งรายชื่อกลับเข้า Telegram
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})

    except Exception as e:
        error_msg = f"❌ **Diagnosis Failed:** {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": error_msg})

if __name__ == "__main__":
    diagnose_system()
