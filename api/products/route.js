// File: /api/products/route.js
import { createClient } from '@supabase/supabase-js';

// เริ่มการเชื่อมต่อกับ Database ผ่าน Environment Variables บน Vercel ปลอดภัย 100%
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function GET(request) {
    try {
        // ดึงข้อมูลสินค้าทั้งหมดจากตาราง 'products' โดยเรียงจากสินค้าที่อัปเดตล่าสุด
        const { data, error } = await supabase
            .from('products')
            .select('*')
            .order('updated_at', { ascending: false });

        if (error) throw error;

        // จัดกลุ่มประเภทสินค้า (Categorization) ให้อยู่ในโครงสร้างที่ Frontend รอรับ
        const structuredData = {
            tech: data.filter(p => p.category === 'tech'),
            organic: data.filter(p => p.category === 'organic'),
            health: data.filter(p => p.category === 'health'),
            utilities: data.filter(p => p.category === 'utilities')
        };

        // ส่งข้อมูลกลับไปที่หน้าเว็บในรูปแบบ JSON ด้วย Edge Runtime ความเร็วสูง
        return new Response(JSON.stringify(structuredData), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=30' 
                // ทำ Caching ที่ Edge Network ของ Vercel เพื่อความเร็วสูงสุด และลดภาระการ Query Database
            }
        });

    } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
