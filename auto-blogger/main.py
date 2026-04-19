import os
import json
import feedparser
import requests
from datetime import datetime

def generate_with_gemini(api_key, prompt):
    # รายชื่อ URL ที่เราจะลอง (เรียงจากอันที่เสถียรที่สุดไปหาอันสำรอง)
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    ]
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for url in endpoints:
        try:
            print(f"กำลังลองเรียก API: {url.split('/')[4]}") # พิมพ์บอกว่าใช้ v1 หรือ v1beta
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"ลองแล้วไม่ได้ (Status {response.status_code}) -> กำลังลองตัวถัดไป...")
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return None

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return

    # ตรวจสอบไฟล์ DB
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
        print(f"--- เริ่มประมวลผล: {feed['name']} ---")
        news = feedparser.parse(feed['url'])
        if not news.entries:
            print("ไม่พบข่าวใหม่")
            continue
        
        entry = news.entries[0]
        products = next((item['products'] for item in affiliate_db if item['category'] == feed['category']), [])
        
        prompt = f"ในนาม CHINPONG SMART FARM สรุปข่าว '{entry.title}' ให้ทุกคนอ่าน (300 คำ) แบบเป็นกันเอง และแนะนำสินค้าเหล่านี้ตอนท้ายแบบเนียนๆ โดยไม่บอกราคาและชื่อแพลตฟอร์ม: {json.dumps(products, ensure_ascii=False)}"
        
        content = generate_with_gemini(api_key, prompt)
        if content:
            filename = f"blog/{datetime.now().strftime('%Y%m%d')}_{feed['category']}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"สร้างบทความสำเร็จ: {filename}")
        else:
            print("บอทพยายามทุกทางแล้วแต่ API ไม่ตอบสนอง")

if __name__ == "__main__":
    main()
