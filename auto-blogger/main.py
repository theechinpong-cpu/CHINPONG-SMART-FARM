import os
import json
import feedparser
import requests
from datetime import datetime

def get_available_models(api_key):
    """ฟังก์ชันสแกนหา Model ที่ Key นี้ใช้ได้จริง"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
            return models
    except:
        return []
    return []

def generate_with_gemini(api_key, prompt):
    # ดึงรายชื่อ Model ที่ใช้ได้จริงจากบัญชีของคุณมาเลย (ไม่ต้องเดาชื่ออีกต่อไป)
    available_models = get_available_models(api_key)
    if not available_models:
        # ถ้าดึงไม่ได้ ให้ใช้ลิสต์มาตรฐานสำรองไว้
        available_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-flash-latest"]
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for model_path in available_models:
        # สร้าง URL ตามชื่อ Model ที่ระบบอนุญาต
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
        try:
            print(f"กำลังลองใช้โมเดลจริงในเครื่องคุณ: {model_path}")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"ตัวนี้ไม่ได้ (Status {response.status_code}) -> ลองตัวถัดไป")
        except:
            continue
    return None

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: 
        print("Error: ลืมใส่ API Key ใน Secrets หรือเปล่าครับ?")
        return

    try:
        with open('data/affiliate_db.json', 'r', encoding='utf-8') as f:
            affiliate_db = json.load(f)
        with open('auto-blogger/rss_feeds.json', 'r', encoding='utf-8') as f:
            rss_feeds = json.load(f)
    except Exception as e:
        print(f"File Error: {e}")
        return

    if not os.path.exists('blog'): os.makedirs('blog')

    for feed in rss_feeds:
        print(f"\n--- Processing: {feed['name']} ---")
        news = feedparser.parse(feed['url'])
        if not news.entries:
            print("No new news entries found.")
            continue
        
        entry = news.entries[0]
        products = next((item['products'] for item in affiliate_db if item['category'] == feed['category']), [])
        
        prompt = f"ในนาม CHINPONG SMART FARM สรุปข่าว '{entry.title}' ให้ทุกคนอ่าน (300 คำ) แบบเป็นกันเอง และแนะนำสินค้าเหล่านี้ตอนท้ายแบบเนียนๆ โดยไม่บอกราคาและชื่อแพลตฟอร์ม: {json.dumps(products, ensure_ascii=False)}"
        
        content = generate_with_gemini(api_key, prompt)
        if content:
            filename = f"blog/{datetime.now().strftime('%Y%m%d')}_{feed['category']}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ สำเร็จ! สร้างบทความที่: {filename}")
        else:
            print("❌ พยายามทุกโมเดลแล้วแต่ API ไม่ยอมรัน")

if __name__ == "__main__":
    main()
