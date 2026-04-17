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
    greetings = ["ไอเทมนี้ดีจริงครับ", "แนะนำอันนี้เลย", "ของมันต้องมี", "ใช้ดีมากครับ", "ชี้เป้าครับ", "พิกัดของดี"]
    product_link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {product_link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    # ใช้ User-Agent ที่ทันสมัยที่สุดเพื่อพรางตัว
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    # ปิดการใช้งาน Automation Flag ที่ X ชอบตรวจจับ
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # ลบค่า Navigator.webdriver เพื่อไม่ให้ X รู้ว่าเป็นบอท
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto;"
    })

    wait = WebDriverWait(driver, 60)
    actions = ActionChains(driver)
    successful_count = 0
    target_goal = 50 

    try:
        print("--- [SYSTEM] เริ่มภารกิจเลียนแบบมนุษย์ ---")
        driver.get("https://x.com/login")

        # 1. Login Step (ปรับให้พิมพ์ช้าลงเหมือนคน)
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        for char in os.getenv("X_USERNAME"):
            user_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        user_field.send_keys(Keys.ENTER)
        time.sleep(5)

        pass_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        for char in os.getenv("X_PASSWORD"):
            pass_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        pass_field.send_keys(Keys.ENTER)
        print("[SUCCESS] ล็อกอินเข้าสู่ระบบ X เรียบร้อย")
        time.sleep(15)

        keywords = ["แจกพิกัด", "รีวิว", "ป้ายยา"]
        
        while successful_count < target_goal:
            query = random.choice(keywords)
            print(f"--- [ROUND] ค้นหา: {query} (สำเร็จแล้ว: {successful_count}/{target_goal}) ---")
            driver.get(f"https://x.com/search?q={query}&f=live")
            time.sleep(10)

            # Scroll หาโพสต์
            driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(5)

            # ดึงลิงก์โพสต์
            post_links = [e.get_attribute('href') for e in driver.find_elements(By.XPATH, '//a[contains(@href, "/status/")]')]
            unique_links = list(dict.fromkeys([l for l in post_links if "/status/" in l]))[:10]

            for url in unique_links:
                if successful_count >= target_goal: break
                
                print(f"กำลังเข้าถึงโพสต์: {url}")
                driver.get(url)
                time.sleep(8)

                try:
                    # คลิกเปิดช่อง Reply ด้วย JavaScript (แก้ปัญหาปุ่มโดนบัง)
                    reply_area = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="reply"]')))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reply_area)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", reply_area)
                    time.sleep(3)

                    # พิมพ์ข้อความทีละตัวเลียนแบบมนุษย์
                    text_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                    comment = get_safe_comment()
                    actions.move_to_element(text_box).click().perform()
                    for char in comment:
                        text_box.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    time.sleep(2)

                    # กดส่ง (คลิกที่ปุ่ม Tweet/Reply)
                    send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                    driver.execute_script("arguments[0].click();", send_btn)
                    
                    successful_count += 1
                    print(f"==> [{successful_count}] ส่งสำเร็จ!")
                    
                    # พักนานขึ้นเพื่อความปลอดภัย (60-120 วินาที)
                    time.sleep(random.randint(60, 120))

                except Exception as e:
                    print(f"ข้ามโพสต์นี้: ตรวจพบอุปสรรค")
                    continue

    except Exception as e:
        print(f"เกิดข้อผิดพลาดร้ายแรง: {e}")
    finally:
        driver.quit()
        print(f"สรุปผลงาน: ส่งได้ทั้งหมด {successful_count} ข้อความ")

if __name__ == "__main__":
    run_bot()
