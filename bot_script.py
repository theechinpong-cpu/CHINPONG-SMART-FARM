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
    greetings = [
        "ไอเทมนี้ดีจริงครับ ลองดู",
        "ใครหาอยู่ แนะนำอันนี้เลย",
        "ของมันต้องมีครับตัวนี้",
        "เพิ่งจัดมาเหมือนกัน ใช้ดีมาก",
        "ชี้เป้าครับ ราคาดีด้วย",
        "พิกัดของดี ตามนี้เลยครับ"
    ]
    # ลิงก์ GitHub Pages ของคุณ
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 45)

    try:
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        print("กำลังเริ่มเข้าสู่ระบบ X...")
        driver.get("https://x.com/login")

        # 1. Login Logic
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(5)

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        print("ล็อกอินสำเร็จ!")
        time.sleep(15)

        # 2. ป้องกัน Pop-up บังหน้าจอ
        driver.refresh()
        time.sleep(10)

        # 3. ค้นหาโพสต์เป้าหมาย
        keywords = ["แจกพิกัด", "ของดีบอกต่อ", "รีวิวจัดโต๊ะคอม"]
        search_query = random.choice(keywords)
        print(f"กำลังค้นหาโพสต์ด้วยคำว่า: {search_query}")
        
        search_url = f"https://x.com/search?q={search_query}&f=live"
        driver.get(search_url)
        time.sleep(12)

        post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/status/")]')))
        target_posts = list(dict.fromkeys([p.get_attribute('href') for p in post_elements if "/status/" in p.get_attribute('href')]))[:2]
        
        print(f"พบเป้าหมาย {len(target_posts)} โพสต์")

        # 4. Loop การ Reply
        for url in target_posts:
            try:
                print(f"กำลังไปที่โพสต์: {url}")
                driver.get(url)
                time.sleep(10)

                comment = get_safe_comment()
                print(f"เตรียมโพสต์ข้อความ: {comment}")

                # ใช้ JavaScript คลิกเพื่อเลี่ยง Pop-up
                reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="reply"]')))
                driver.execute_script("arguments[0].click();", reply_btn)
                time.sleep(5)

                text_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                text_area.send_keys(comment)
                time.sleep(3)

                send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                driver.execute_script("arguments[0].click();", send_btn)
                
                print("--- ส่งคอมเมนต์สำเร็จ! ---")
                time.sleep(30)

            except Exception as e:
                print(f"ข้ามโพสต์เนื่องจาก: {e}")
                continue

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        driver.quit()
        print("จบการทำงาน")

if __name__ == "__main__":
    run_bot()
