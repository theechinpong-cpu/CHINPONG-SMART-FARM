import random
import time

def get_safe_comment():
    # 1. รายการข้อความเกริ่นนำ (Human-like)
    greetings = [
        "ไอเทมนี้ดีจริงครับ ลองดู",
        "ใครหาอยู่ แนะนำอันนี้เลย",
        "ของมันต้องมีครับตัวนี้",
        "เพิ่งจัดมาเหมือนกัน ใช้ดีมาก",
        "ชี้เป้าครับ ราคาดีด้วย"
    ]
    
    # 2. รายการลิงก์ (อาจจะใช้ลิงก์ตรงสลับกับลิงก์ที่ย่อมาใหม่)
    product_links = [
        "https://s.shopee.co.th/2g5bPAW1Fg",
        "https://s.shopee.co.th/2g5bPAW1Fg?smtt=0.0.9" # ใส่ parameter หลอกเพื่อให้ URL ไม่ซ้ำ
    ]
    
    message = f"{random.choice(greetings)} {random.choice(product_links)}"
    return message

# ตอนสั่ง Selenium พิมพ์
# comment_text = get_safe_comment()
# textbox.send_keys(comment_text)
