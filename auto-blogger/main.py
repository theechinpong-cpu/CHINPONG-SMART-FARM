import os

# แก้ไขส่วนนี้โดยห้ามมีย่อหน้า (Space) ด้านหน้าตัวแปร prompt
def generate_prompt():
    prompt = f"""
เขียนบทความข่าวไอทีและเทคโนโลยีสำหรับเว็บไซต์ CHINPONG SMART FARM 
โดยให้เน้นเนื้อหาที่อ่านง่าย สนุก และเป็นกันเอง 
ความยาวประมาณ 500-800 คำ 
และให้แทรกข้อความ "(ใส่ลิงก์ Affiliate ของคุณตรงนี้)" 
ลงในเนื้อหาอย่างน้อย 2-3 จุด ในตำแหน่งที่เหมาะสมกับสินค้าประเภท Gadget หรืออุปกรณ์ไอที
"""
    return prompt

def main():
    # ตรวจสอบว่า Code ส่วนอื่นของพี่ทำงานปกติ
    print("Starting Auto-Blogger...")
    try:
        # ตัวอย่างการทำงาน
        content_prompt = generate_prompt()
        print("Prompt Generated Successfully")
        # ส่วนเชื่อมต่อ API หรือการเขียนไฟล์ของพี่...
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
