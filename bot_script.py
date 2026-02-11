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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def get_safe_comment():
    greetings = ["ไอเทมนี้ดีจริงครับ", "แนะนำอันนี้เลย", "ของมันต้องมี", "ใช้ดีมากครับ", "ชี้เป้าครับ", "พิกัดของดี", "ลองดูอันนี้"]
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    # ใช้ User-Agent ที่ดูเป็นมนุษย์ที่สุด
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 60)
    actions = ActionChains(driver)

    successful_count = 0
    target_goal = 50 

    try:
        username = os.getenv("X_USERNAME")
        password = os.getenv("X_PASSWORD")

        print("--- เริ่มกระบวนการล็อกอิน ---")
        driver.get("https://x.com/login")

        # Login Step
        wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(username, Keys.ENTER)
        time.sleep(7)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password, Keys.ENTER)
        print("ล็อกอินสำเร็จ!")
        time.sleep(20)

        keywords = ["แจกพิกัด", "รีวิว", "ป้ายยา", "ของดีบอกต่อ"]
        
        while successful_count < target_goal:
            query = random.choice(keywords)
            print(f"ค้นหา: {query} (สำเร็จแล้ว: {successful_count}/{target_goal})")
            driver.get(f"https://x.com/search?q={query}&f=live")
            time.sleep(15)

            # Scroll เพื่อโหลดโพสต์ใหม่ๆ
            driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(5)

            # ดึงลิงก์โพสต์ (XPath ที่เจาะจงมากขึ้น)
            post_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/status/")]')
            target_links = list(dict.fromkeys([p.get_attribute('href') for p in post_elements if "/status/" in p.get_attribute('href')]))
            
            for url in target_links:
                if successful_count >= target_goal: break
                
                print(f"กำลังไปที่: {url}")
                driver.get(url)
                time.sleep(12)

                try:
                    # ใช้ JavaScript คลิกเพื่อเปิดช่อง Reply
                    reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="reply"]')))
                    driver.execute_script("arguments[0].click();", reply_btn)
                    time.sleep(5)

                    # ใช้ ActionChains เพื่อพิมพ์ข้อความทีละตัว (เลียนแบบคน)
                    text_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                    comment = get_safe_comment()
                    actions.move_to_element(text_area).click().send_keys(comment).perform()
                    print(f"พิมพ์ข้อความ: {comment}")
                    time.sleep(5)

                    # คลิกส่ง
                    send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                    driver.execute_script("arguments[0].click();", send_btn)
                    
                    successful_count += 1
                    print(f"--- [{successful_count}] ส่งสำเร็จ! ---")
                    
                    # พักระหว่างโพสต์ (สำคัญมาก!)
                    time.sleep(random.randint(45, 90))

                except Exception as e:
                    print(f"ข้ามโพสต์เนื่องจากติดขัด: {e}")
                    continue

    except Exception as e:
        print(f"เกิดข้อผิดพลาดร้ายแรง: {e}")
    finally:
        driver.quit()
        print(f"จบการทำงาน สรุปส่งได้: {successful_count}")

if __name__ == "__main__":
    run_bot()
