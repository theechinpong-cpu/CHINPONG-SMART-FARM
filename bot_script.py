import os, random, time
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
    link = "https://theechinpong-cpu.github.io/king-mongkut-tutor/go.html"
    return f"{random.choice(greetings)} {link}"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 40)

    try:
        # Login
        driver.get("https://x.com/login")
        wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(os.getenv("X_USERNAME"), Keys.ENTER)
        time.sleep(5)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(os.getenv("X_PASSWORD"), Keys.ENTER)
        print("Login Attempted")
        time.sleep(15)

        # จัดการหน้าต่างขวาง (Force Refresh)
        driver.get("https://x.com/search?q=%E0%B9%81%E0%B8%88%E0%B8%81%E0%B8%92%E0%B8%B4%E0%B8%81%E0%B8%B1%E0%B8%94&f=live")
        time.sleep(10)

        # ค้นหาโพสต์และดึงลิงก์
        posts = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/status/")]')))
        urls = list(set([p.get_attribute('href') for p in posts]))[:2]

        for url in urls:
            driver.get(url)
            time.sleep(8)
            try:
                # ใช้ JavaScript คลิกเพื่อแก้ปัญหาปุ่มถูกบัง (Force Click)
                reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="reply"]')))
                driver.execute_script("arguments[0].click();", reply_btn)
                
                text_input = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
                text_input.send_keys(get_safe_comment())
                time.sleep(3)
                
                send_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                driver.execute_script("arguments[0].click();", send_btn)
                print(f"Post Sent to {url}")
                time.sleep(20)
            except:
                continue
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
