# ปรับ Prompt ให้ AI สร้างเนื้อหาแบบ Magazine
        prompt = f"""
        ในฐานะ CHINPONG SMART FARM ช่วยเขียนบทความ Blog จากข่าวนี้:
        หัวข้อข่าว: {entry.title}
        เนื้อหาสรุป: {entry.summary if 'summary' in entry else entry.title}
        
        กฎการเขียนสำหรับ Magazine Style:
        1. สรุปข่าวประมาณ 300 คำ ใช้ภาษาเป็นกันเอง (สรรพนาม: ทุกคน)
        2. หาภาพที่เกี่ยวข้องกับข่าวมาใส่ 1 ภาพ (ใช้รูปแบบ Markdown: ![ภาพประกอบ]({entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else 'https://via.placeholder.com/600x400'}) )
        3. เลือกสินค้า 1 ชิ้นจากรายการนี้: {json.dumps(products, ensure_ascii=False)}
        4. ปิดท้ายด้วยปุ่มกดซื้อสินค้า โดยใช้รูปแบบ Markdown เด่นๆ:
           [👉 กดสั่งซื้อสินค้าคุณภาพสูงที่นี่! ({products[0]['name'] if products else 'สินค้าแนะนำ'}) ]({products[0]['link'] if products else '#'}){{: .btn .btn--primary }}
           
        *ห้ามบอกราคา ห้ามบอกชื่อแพลตฟอร์ม*
        """
