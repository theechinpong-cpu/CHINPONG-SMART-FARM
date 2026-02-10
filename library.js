// ==========================================
// 🛍️ คลังสินค้า Shopee Affiliate (Smart Database 2026)
// ==========================================
const shopeeLibrary = [
    { name: "ติวเข้ม เก่ง 5 วิชา สอบเข้า ม.1 โรงเรียนชื่อดัง", cat: "Study", link: "https://s.shopee.co.th/6VIIqbVqK9", highlight: "สรุปครบทั้ง วิทย์-คณิต-อังกฤษ-ไทย-สังคม ในเล่มเดียว คุ้มมากครับ" },
    { name: "เตรียมสอบ ม.3 เข้า ม.4 ฉบับสมบูรณ์ อัปเดตครั้งที่ 1", cat: "Study", link: "https://s.shopee.co.th/2B9JgbvoFW", highlight: "เนื้อหาอัปเดตล่าสุด เตรียมตัวสอบเข้า ม.4 แบบมั่นใจ" },
    { name: "เตรียมสอบ ป.6 เข้า ม.1 ฉบับสมบูรณ์ (SE-ED)", cat: "Study", link: "https://s.shopee.co.th/5L6LSZbNKB", highlight: "เล่มนี้ละเอียดมาก เหมาะสำหรับเด็กๆ ที่จะสอบเข้าโรงเรียนดัง" },
    { name: "5 วิชาติวเข้มสอบเข้า ม.1 (ฉบับปรับปรุง 2024)", cat: "Study", link: "https://s.shopee.co.th/4fqefMdVdD", highlight: "ฉบับปรับปรุงใหม่ล่าสุดปี 2024 รวมแนวข้อสอบที่ออกบ่อย" },
    { name: "แนวข้อสอบ ป.6 เข้า ม.1 (รวม 5 วิชา) + Gifted/EP", cat: "Study", link: "https://s.shopee.co.th/5AmvGIxoqg", highlight: "มีแนวข้อสอบห้อง Gifted และ EP โดยเฉพาะ ท้าทายความสามารถสุดๆ" },
    { name: "ติวเข้มเก่ง 5 วิชา สอบเข้า ม.1 (สนพ.เอ็มไอเอส)", cat: "Study", link: "https://s.shopee.co.th/4AuO4UcxnQ", highlight: "เขียนโดยกลุ่มวิชาการ Get Good Grade สรุปสั้นเข้าใจง่าย" },
    { name: "นายอินทร์: ติวเข้มเก่ง 5 วิชา สอบเข้า ม.1", cat: "Study", link: "https://s.shopee.co.th/20ptUX82mZ", highlight: "หนังสือขายดีจากนายอินทร์ รวมเทคนิคทำข้อสอบให้ไว" },
    { name: "สรุปย่อ + ข้อสอบ ป.6 All-in-One พร้อมสอบ O-NET", cat: "Study", link: "https://s.shopee.co.th/AABbDYoeL9", highlight: "เล่มเดียวจบ! ได้ทั้งสอบเข้า ม.1 และสอบ O-NET ปรับปรุงใหม่ครั้งที่ 2" },
    { name: "เก่งชัวร์ คู่มือสอบคณิตศาสตร์เข้า ม.1", cat: "Math", link: "https://s.shopee.co.th/3VehHK95UX", highlight: "เน้นคณิตศาสตร์แบบเจาะลึก ใครอยากเก็บคะแนนวิชานี้ต้องเล่มนี้เลย" },
    { name: "เตรียมสอบ ป.6 เข้า ม.1 ฉบับสมบูรณ์ (Think Beyond)", cat: "Study", link: "https://s.shopee.co.th/20ptUa7Nk8", highlight: "รวมเนื้อหาจากหลายสำนักพิมพ์ดัง ครบถ้วนทุกประเด็นสำคัญ" },
    { name: "ตะลุยข้อสอบ อังกฤษ ป.6 เตรียมสอบเข้า ม.1", cat: "English", link: "https://s.shopee.co.th/14p6v1Sfb", highlight: "เน้นภาษาอังกฤษล้วนๆ ฝึกทำโจทย์ให้ชินก่อนลงสนามจริง" },
    { name: "เตรียมสอบ ม.3 เข้า ม.4 (Thinkbeyond Book)", cat: "Study", link: "https://s.shopee.co.th/9pYkp0CDXM", highlight: "คู่มือเตรียมตัวสอบเข้า ม.4 ที่สมบูรณ์ที่สุด อัปเดตเนื้อหาใหม่" },
    { name: "Super Maths / Super Science สรุป ม.ต้น", cat: "Science", link: "https://s.shopee.co.th/3fy7TgLx8S", highlight: "สรุปวิทย์-คณิต ม.ต้น แบบเน้นๆ สำหรับสอบเข้า ม.4" },
    { name: "ติวเข้ม เก่ง 5 วิชา สอบเข้า ม.1 (ฉบับเร่งรัด)", cat: "Study", link: "https://s.shopee.co.th/5VPlf4WNHc", highlight: "เวลาน้อยต้องเล่มนี้! สรุปเนื้อหาสำคัญแบบเร่งรัดก่อนสอบ" },
    { name: "ฟิสิกส์ ม.4-6 ครบทุกเล่ม ฉบับช่วยสอบเข้ามหาวิทยาลัย", cat: "Science", link: "https://s.shopee.co.th/3LLH56Mgls", highlight: "สำหรับรุ่นพี่ ม.ปลาย เตรียมสอบรับตรง โควต้า และ PAT2" },
    { name: "ติวเข้มเก่ง 5 วิชา สอบเข้า ม.1 (ฉบับเร่งรัด SE-ED)", cat: "Study", link: "https://s.shopee.co.th/4VXETG8QQl", highlight: "ติวเข้มหน้าสุดท้ายก่อนเข้าห้องสอบ สรุปประเด็นหลักให้แม่น" },
    { name: "สรุปเนื้อหา 5 วิชา เตรียมสอบเข้า ม.1", cat: "Study", link: "https://s.shopee.co.th/8Kjx2Jgdph", highlight: "สรุปเนื้อหาอ่านง่าย มีภาพประกอบ ช่วยให้จำได้ดีขึ้น" },
    { name: "ติวเข้ม ป.6 สอบเข้า ม.1 พิชิตข้อสอบเต็ม", cat: "Study", link: "https://s.shopee.co.th/1qWTINnB41", highlight: "รวมแนวข้อสอบจริง ฝึกทำเยอะๆ จะได้ไม่ประหม่าเวลาสอบครับ" }
];

// --- แคปชันสำหรับป้ายยา (สุ่มอัตโนมัติ) ---
const affCaps = [
    "ชาว [CAT] ต้องมี! [NAME] ตัวนี้ [HIGHLIGHT] แอดคัดมาให้แล้ว พิกัดร้านในคอมเมนต์นะ 👇✨",
    "ไอเทมเด็ดที่เด็กๆ ต้องชอบ! ✨ [NAME] [HIGHLIGHT] แปะลิงก์ร้านที่แอดซื้อประจำไว้ให้แล้ว 👇",
    "ของดีบอกต่อครับ! 😂 [NAME] สวยตรงปก ใช้งานดีมาก [HIGHLIGHT] กดดูได้เลยที่คอมเมนต์ 👇"
];
