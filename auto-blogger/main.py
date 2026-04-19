import os
import json
import feedparser
from google import genai
from datetime import datetime

# รายชื่อ Model สำรอง กรณีตัวหลักใช้ไม่ได้
MODEL_PRIORITY = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # ... (โหลดข้อมูลตามปกติ) ...
    
    for feed in rss_feeds:
        # ... (ดึงข่าวตามปกติ) ...
        
        success = False
        for model_name in MODEL_PRIORITY:
            if success: break
            try:
                print(f"ลองใช้ model: {model_name}")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                # บันทึกไฟล์...
                success = True
            except Exception as e:
                print(f"Model {model_name} มีปัญหา: {e} -> กำลังลองตัวสำรอง...")
