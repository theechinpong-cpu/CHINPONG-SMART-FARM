import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime

# --- Configuration ---
# แนะนำให้ตั้งค่า GEMINI_API_KEY ใน GitHub Secrets
GENAI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GENAI_API_KEY)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_latest_news(rss_url):
    feed = feedparser.parse(rss_url)
    if feed.entries:
        # ดึงมาเฉพาะข่าวล่าสุด 1 ข่าว เพื่อป้องกันการทำงานหนักเกินไปในแต่ละรอบ
        entry = feed.entries[0]
        return {
            "title": entry.title,
            "link": entry.link,
            "description": entry.summary if 'summary' in entry else ""
        }
    return None

def generate_content(news_data, category, affiliate_db):
    # คัดเลือกสินค้าที่ตรงกับหมวดหมู่
    relevant_products = next((item['products'] for item in affiliate_db if item['category'] == category), [])
    product_context = json.dumps(relevant_products, ensure_ascii=False)

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    คุณคือคอนเทนต์ครีเอเตอร์มืออาชีพของ CHINPONG SMART FARM
    จงสรุปข่าวนี้ให้ดูน่าสนใจ เข้าใจง่าย สำหรับ "ทุกคน" (ใช้คำว่าทุกคนแทนคุณ)
    
    หัวข้อข่าว: {news_data['title']}
    เนื้อหาข่าวโดยสรุป: {news_data['description']}
    
    กฎเหล็ก:
    1. ห้ามระบุราคา ห้ามระบุชื่อแพลตฟอร์ม (เช่น Shopee, TikTok) 
    2. ห้ามมีลิงก์ภายนอกอื่นนอกจากที่กำหนดให้
    3. สรุปเนื้อหาประมาณ 300-400 คำ
    
    จากนั้น ให้เลือกสินค้า 1 อย่างจากรายการด้านล่างนี้ที่เข้ากับเนื้อหาข่าวที่สุด 
    และเขียนแนะนำสินค้าท้ายบทความให้แนบเนียน พร้อมแนบลิงก์ที่ให้มา:
    รายการสินค้า: {product_context}
    
    รูปแบบผลลัพธ์: ให้ส่งกลับมาเป็น Markdown (มีหัวข้อข่าว, เนื้อหาสรุป, และส่วนแนะนำสินค้า)
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    # 1. Load Data
    affiliate_db = load_json('data/affiliate_db.json')
    rss_feeds = load_json('auto-blogger/rss_feeds.json')
    
    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    output_dir = 'blog'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for feed in rss_feeds:
        print(f"Processing: {feed['name']}...")
        news = get_latest_news(feed['url'])
        
        if news:
            # 2. Generate Content with AI
            content = generate_content(news, feed['category'], affiliate_db)
            
            # 3. Save to File
            filename = f"{datetime.now().strftime('%Y%m%d')}_{feed['category']}.md"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved: {file_path}")

if __name__ == "__main__":
    main()
