import os
import json
import feedparser
import requests
from datetime import datetime

def generate_with_gemini(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return None

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return

    # Load Database
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
        print(f"Fetching: {feed['name']}")
        news = feedparser.parse(feed['url'])
        if not news.entries: continue
        
        entry = news.entries[0]
        products = next((item['products'] for item in affiliate_db if item['category'] == feed['category']), [])
        
        prompt = f"ในนาม CHINPONG SMART FARM สรุปข่าว '{entry.title}' ให้ทุกคนอ่าน (300 คำ) สไตล์เป็นกันเอง ห้ามบอกราคา/ชื่อแพลตฟอร์ม และแนะนำสินค้าจากรายการนี้ตอนท้าย: {json.dumps(products, ensure_ascii=False)}"
        
        content = generate_with_gemini(api_key, prompt)
        if content:
            filename = f"blog/{datetime.now().strftime('%Y%m%d')}_{feed['category']}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Success: {filename}")

if __name__ == "__main__":
    main()
