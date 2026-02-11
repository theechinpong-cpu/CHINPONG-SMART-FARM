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
        "ชี้เป้าครับ ราคาดีด้วย"
    ]
    # ลิงก์ Shield ผ่าน GitHub Pages
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
    wait = WebDriverWait(driver, 30)

    try:
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        print("--- เริ่มการทำงาน ---")
        driver.get("https://x.com/login")

        # 1. Login
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(3)

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        print("Login สำเร็จ!")
        time.sleep(10)

        # 2. จัดการหน้าต่าง Premium/Pop-up
        print("ตรวจสอบ Pop-up...")
        driver.refresh() # รีเฟรชเพื่อล้างหน้าต่างเด้ง
        time.sleep(10)

        # 3. Discovery (ค้นหา)
        keywords = ["แจกพิกัด", "ของดีบอกต่อ", "รีวิวจัดโต๊ะคอม"]
        search_query = random.choice(keywords)
        print(f"กำลังค้นหา: {search_query}")
        
        driver.get(f"https://x.com/search?q={search_query}&f=live")
        time.sleep(10)

        # เก็บภาพหน้าจอเพื่อเช็คว่าเห็นอะไร (Debug)
        driver.save_screenshot('search_result.png')

        post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/status/")]')))
        target_posts = list(set([post.get_attribute('href') for post in post_elements if "/status/" in post.get_attribute('href')]))[:2]
        
        print(f"พบเป้าหมาย {len(target_posts)} โพสต์")

        # 4. Reply Loop
        for url in target_posts:
            try:
                print(f"กำลังไปที่: {url}")
                driver.get(url)
                time.sleep(10)

                # กดปุ่มตอบกลับ
                reply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="reply"]')))
                reply_btn.click()
                time.sleep(3)

                text_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                comment = get_safe_comment()
                text_area.send_keys(comment)
                time.sleep(3)

                send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                send_btn.click()
                
                print(f"โพสต์สำเร็จ: {comment}")
                time.sleep(20)

            except Exception as inner_e:
                print(f"ข้ามโพสต์ {url} เนื่องจากมีสิ่งกีดขวางหรือหาปุ่มไม่เจอ")
                continue

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        driver.save_screenshot('error_debug.png')
    finally:
        driver.quit()
        print("--- จบการทำงาน ---")

if __name__ == "__main__":
    run_bot()
