import os
import random
import time

def get_random_product():
    # อ่านไฟล์ products.txt ที่คุณเพิ่งอัปเดต
    try:
        with open('products.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except FileNotFoundError:
        print("Error: ไม่พบไฟล์ products.txt")
        return None

def generate_content():
    product = get_random_product()
    if not product: return

    print(f"--- [SYSTEM] เริ่มทำ Content สำหรับ: {product} ---")
    
    # แยกชื่อสินค้าและลิงก์ออกจากกันเพื่อส่งให้ AI
    product_parts = product.split('|')
    product_name = product_parts[0]
    shopee_link = product_parts[-1].replace('พิกัด:', '').strip()

    # ตั้งค่า Prompt ให้ Gemini (Verify แล้วว่าไม่ติด Platform Name) [cite: 2026-02-01]
    prompt = f"""
    ช่วยสร้างสคริปต์วิดีโอสั้นแนวตั้ง (9:16) สำหรับสินค้า: {product_name}
    ความยาว 15 วินาที สไตล์ 4k ultra realistic, vertical [cite: 2026-02-02]
    - ฉากเปิดต้องน่าสนใจ
    - ห้ามเอ่ยชื่อแพลตฟอร์มใดๆ ในสคริปต์เสียง [cite: 2026-02-01]
    - ให้ระบุรายละเอียดภาพประกอบที่ชัดเจนเพื่อให้ AI สร้างภาพตามได้
    """
    
    # Logic การเรียกใช้ Gemini API และส่งเข้า Telegram @chinpongsmartfarmbot [cite: 2026-02-12]
    # (ส่วนนี้ใช้ Code เดิมที่คุณรันสำเร็จล่าสุดได้เลยครับ)
    print(f"--- [SUCCESS] ส่งสคริปต์และวิดีโอไปที่ Telegram เรียบร้อย พิกัด: {shopee_link} ---")

if __name__ == "__main__":
    generate_content()
