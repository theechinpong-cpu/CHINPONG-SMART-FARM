import os
import json
import gspread
from google.oauth2.service_account import Credentials

def update_dashboard():
    try:
        # 1. โหลดสิทธิ์จาก GitHub Secrets ที่เราตั้งค่าไว้
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        # ดึงข้อมูล JSON จาก Environment Variable
        service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(creds)

        # 2. เชื่อมต่อกับ Google Sheet ของคุณ
        # ใช้ Sheet ID เดิมที่คุณเคยใช้ในหน้าเว็บ
        SHEET_ID = "1oGTv23WfGJMu_TGWzMzc9R-CUeNp_TMIWxjNy25z1A4"
        spreadsheet = client.open_by_key(SHEET_ID)
        # เลือกหน้า Sheet (ถ้าชื่ออื่นให้แก้ 'Sheet1' เป็นชื่อนั้น)
        worksheet = spreadsheet.worksheet('Sheet1') 

        # 3. เตรียมข้อมูล (Mock Data)
        # ในอนาคตคุณจะเขียนโค้ดดึงข้อมูลจริงจาก Shopee/TikTok ตรงนี้
        # ตัวอย่างข้อมูล: [ชื่อสินค้า, ยอดวิว, ยอดขาย, ค่าคอม]
        update_data = [
            ["สินค้าตัวท็อป", "15,200", "450,000", "22,500"],
            ["สินค้าแนะนำ", "8,900", "120,000", "6,000"]
        ]

        # 4. อัปเดตข้อมูลลงใน Sheet เริ่มจากแถวที่ 2 (A2)
        # เพื่อไม่ให้ทับหัวตาราง (Header) ในแถวที่ 1
        worksheet.update('A2:D3', update_data)

        print("✅ การอัปเดตข้อมูลสำเร็จ: ข้อมูลใหม่ถูกส่งไปยัง Google Sheet แล้ว")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    update_dashboard()
