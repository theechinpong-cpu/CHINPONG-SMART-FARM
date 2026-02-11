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
    greetings = ["ไอเทมนี้ดีจริงครับ", "แนะนำอันนี้เลย", "ของมันต้องมี", "ใช้ดีมากครับ", "ชี้เป้าครับ"]
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 60) # เพิ่มเวลารอเป็น 60 วินาที

    try:
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        print("--- เริ่มกระบวนการล็อกอิน ---")
        driver.get("https://x.com/login")

        # Login Step
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(7)

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        print("ล็อกอินสำเร็จ!")
        time.sleep(20)

        # ค้นหาโพสต์
        keywords = ["แจกพิกัด", "รีวิว"]
        search_query = random.choice(keywords)
        driver.get(f"https://x.com/search?q={search_query}&f=live")
        time.sleep(15)

        # ดึงโพสต์เป้าหมาย
        post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/status/")]')))
        target_links = list(dict.fromkeys([p.get_attribute('href') for p in post_elements if "/status/" in p.get_attribute('href')]))[:1]
        
        for url in target_links:
            print(f"กำลังไปที่โพสต์: {url}")
            driver.get(url)
            time.sleep(12)

            # --- จุดตาย: การกด Reply ---
            try:
                # 1. พิมพ์ข้อความลงไปตรงๆ (ไม่ต้องรอคลิกปุ่ม Reply ก่อน เพื่อลดความเสี่ยง)
                text_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                comment = get_safe_comment()
                driver.execute_script("arguments[0].innerText = arguments[1];", text_area, comment) # บังคับใส่ Text
                text_area.send_keys(Keys.SPACE) # กระตุ้นให้ปุ่มส่งทำงาน
                print(f"ใส่ข้อความเรียบร้อย: {comment}")
                time.sleep(5)

                # 2. บังคับกดส่งด้วย JS หลายช่องทาง
                send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", send_btn)
                driver.execute_script("arguments[0].click();", send_btn)
                
                print("--- [CONFIRMED] ส่งคอมเมนต์เรียบร้อย! ---")
                time.sleep(10)

            except Exception as e:
                print(f"ส่งไม่สำเร็จในโพสต์นี้: {e}")

    except Exception as e:
        print(f"เกิดข้อผิดพลาดร้ายแรง: {e}")
    finally:
        driver.quit()
        print("--- จบการทำงาน ---")

if __name__ == "__main__":
    run_bot()
