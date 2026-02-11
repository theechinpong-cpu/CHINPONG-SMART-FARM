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
    # รายการข้อความสุ่มเพื่อเลี่ยงการตรวจจับ Spam
    greetings = [
        "ไอเทมนี้ดีจริงครับ ลองดู",
        "ใครหาอยู่ แนะนำอันนี้เลย",
        "ของมันต้องมีครับตัวนี้",
        "เพิ่งจัดมาเหมือนกัน ใช้ดีมาก",
        "ชี้เป้าครับ ราคาดีด้วย"
    ]
    # ลิงก์ผ่าน GitHub Pages (Link Shield)
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless') # รันเบื้องหลังบน GitHub Actions
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        # ดึงค่าจาก Secrets
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        if not username or not password:
            print("Error: ไม่พบ X_USERNAME หรือ X_PASSWORD ใน Secrets")
            return

        # --- ขั้นตอนการ Login ---
        print("กำลังเข้าสู่หน้า Login...")
        driver.get("https://x.com/login")

        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(3)

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        print("Login สำเร็จ!")
        
        # --- จัดการ Pop-up ที่ขวางหน้าจอ (เช่นหน้า Premium) ---
        time.sleep(10)
        print("ตรวจสอบและจัดการหน้าต่างขวางกั้น...")
        driver.refresh() # รีเฟรชเพื่อล้างหน้าต่างโฆษณาที่มักเด้งตอน Login ครั้งแรก
        time.sleep(7)

        # --- ขั้นตอนการค้นหาโพสต์อัตโนมัติ ---
        keywords = ["แจกพิกัด", "ของดีบอกต่อ", "รีวิวจัดโต๊ะคอม"]
        search_query = random.choice(keywords)
        print(f"กำลังค้นหาด้วยคำว่า: {search_query}")
        
        search_url = f"https://x.com/search?q={search_query}&f=live"
        driver.get(search_url)
        time.sleep(10)

        # ดึงลิงก์โพสต์
        post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/status/")]')))
        target_posts = list(set([post.get_attribute('href') for post in post_elements if "/status/" in post.get_attribute('href')]))[:3]
        
        print(f"พบเป้าหมาย {len(target_posts)} โพสต์")

        # --- ลูปการตอบกลับ ---
        for url in target_posts:
            try:
                print(f"กำลังไปที่: {url}")
                driver.get(url)
                time.sleep(7)

                # กดปุ่ม Reply (ใช้ XPath ที่เจาะจงมากขึ้น)
                reply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="reply"]')))
                reply_btn.click()
                time.sleep(2)

                # พิมพ์ข้อความ
                text_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                comment = get_safe_comment()
                text_area.send_keys(comment)
                time.sleep(2)

                # กดส่ง
                send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                send_btn.click()
                
                print(f"สำเร็จ: {comment}")
                time.sleep(random.randint(20, 40)) # รอเพื่อความเป็นธรรมชาติ

            except Exception as inner_e:
                print(f"ข้ามโพสต์นี้เนื่องจากปุ่มถูกบังหรือหาไม่เจอ")
                continue

    except Exception as e:
        print(f"เกิดข้อผิดพลาดร้ายแรง: {e}")
    finally:
        driver.quit()
        print("ปิดระบบ")

if __name__ == "__main__":
    run_bot()
