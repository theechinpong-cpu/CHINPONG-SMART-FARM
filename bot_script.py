import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_safe_comment():
    # 1. รายการข้อความเกริ่นนำ (Human-like)
    greetings = [
        "ไอเทมนี้ดีจริงครับ ลองดู",
        "ใครหาอยู่ แนะนำอันนี้เลย",
        "ของมันต้องมีครับตัวนี้",
        "เพิ่งจัดมาเหมือนกัน ใช้ดีมาก",
        "ชี้เป้าครับ ราคาดีด้วย"
    ]
    # 2. ลิงก์ผ่าน GitHub Pages เพื่อความปลอดภัย
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    # Setup Chrome Options สำหรับรันบน Cloud (GitHub Actions)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        # ดึงค่าจาก GitHub Secrets
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        if not username or not password:
            print("Error: ไม่พบ X_USERNAME หรือ X_PASSWORD ใน Secrets")
            return

        print("กำลังเข้าสู่หน้า Login ของ X...")
        driver.get("https://x.com/login")

        # 1. กรอก Username
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # 2. กรอก Password
        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        print("Login สำเร็จ!")
        time.sleep(5)

        # 3. เตรียมข้อความ
        message = get_safe_comment()
        print(f"เตรียมโพสต์ข้อความ: {message}")

        # --- ขั้นตอนถัดไป: ใส่ URL ของโพสต์เป้าหมายที่นี่ ---
        # ตัวอย่าง:
        # target_url = "URL_ของโพสต์ที่ยอดวิวสูง"
        # driver.get(target_url)
        # ... ใส่ Logic การกด Reply ...

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        driver.quit()
        print("ปิดเบราว์เซอร์ เรียบร้อย")

if __name__ == "__main__":
    run_bot()
