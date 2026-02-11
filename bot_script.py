import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_safe_comment():
    greetings = [
        "ไอเทมนี้ดีจริงครับ ลองดู",
        "ใครหาอยู่ แนะนำอันนี้เลย",
        "ของมันต้องมีครับตัวนี้",
        "เพิ่งจัดมาเหมือนกัน ใช้ดีมาก",
        "ชี้เป้าครับ ราคาดีด้วย"
    ]
    # เปลี่ยนเป็นลิงก์ GitHub Pages เพื่อความปลอดภัย
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    # 1. Setup Chrome Options สำหรับรันบน Cloud
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 2. ดึงค่าจาก GitHub Secrets
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        print("กำลังเริ่มเข้าสู่ระบบ X...")
        driver.get("https://x.com/login")
        time.sleep(10) # รอหน้าเว็บโหลด

        # --- Logic การ Login และโพสต์จะเริ่มตรงนี้ ---
        # Note: คุณสามารถเพิ่ม XPath เพื่อสั่งพิมพ์ User/Pass ได้ที่นี่
        
        comment = get_safe_comment()
        print(f"เตรียมโพสต์ข้อความ: {comment}")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
