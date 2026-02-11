// menu.js - คลังข้อมูลบทเรียนทั้งหมด
const lessonMenu = [
    {
        category: "ประถมศึกษา ป.1 - ป.6",
        color: "green",
        icon: "fas fa-book-reader",
        items: [
            {
                subject: "ภาษาอังกฤษ (ป.5 เทอม 2)",
                icon: "🇬🇧",
                links: [
                    { title: "คลังคำศัพท์ (1,200 คำ)", url: "vocabulary-pri-5-1.html", type: "normal" },
                    { title: "ทบทวนศัพท์ 1-10 (Liverpool)", url: "liverpool-lesson.html", type: "italic" },
                    { title: "🎯 ข้อสอบปลายภาค", url: "korsob-plaiterm-2.html", type: "bold" }
                ]
            },
            {
                subject: "ภาษาไทย (ป.5)",
                icon: "🇹🇭",
                links: [
                    { title: "คำศัพท์ภาษาไทย", url: "thai-p5-vocab.html", type: "normal" },
                    { title: "หลักภาษาและการใช้ภาษา", url: "thai-p5-lesson.html", type: "normal" },
                    { title: "แนวข้อสอบภาษาไทย", url: "thai-p5-exam.html", type: "bold" }
                ]
            },
            {
                subject: "สังคม / ประวัติ / ศาสนา",
                icon: "🗺️",
                links: [
                    { title: "บทเรียนพระพุทธศาสนา", url: "social-p5-religion.html", type: "normal" },
                    { title: "หน้าที่พลเมืองและวัฒนธรรม", url: "social-p5-duty.html", type: "normal" },
                    { title: "ประวัติศาสตร์ไทย ป.5", url: "social-p5-history.html", type: "normal" },
                    { title: "ภูมิศาสตร์ไทย", url: "social-p5-geography.html", type: "normal" },
                    { title: "รวมข้อสอบสังคมศึกษา", url: "social-exam-all.html", type: "bold" }
                ]
            },
            {
                subject: "วิทย์ - คณิต (ป.5)",
                icon: "🧪",
                links: [
                    { title: "วิทยาศาสตร์ ป.5 เทอม 2", url: "science-p5-t2.html", type: "bold" },
                    { title: "คณิตศาสตร์ ป.5 เทอม 2", url: "math-p5-t2.html", type: "bold" }
                ]
            }
        ]
    },
    {
        category: "มัธยมศึกษา ม.1 - ม.6",
        color: "red",
        icon: "fas fa-user-graduate",
        items: [
            {
                subject: "Culinary English (ม.4)",
                icon: "👨‍🍳",
                links: [
                    { title: "คลังคำศัพท์ Chef JOURNEY", url: "vocabulary-m4-chef.html", type: "bold" },
                    { title: "บทเรียน Chef's English", url: "chef-lesson.html", type: "italic" }
                ]
            },
            {
                subject: "วิทยาศาสตร์ชีวภาพ (ม.ปลาย)",
                icon: "🧬",
                links: [
                    { title: "บทที่ 1: การลำเลียงสาร", url: "cell-transport.html", type: "normal" },
                    { title: "บทที่ 2: ดุลยภาพร่างกาย", url: "homeostasis.html", type: "normal" }
                ]
            },
            {
                subject: "สังคมศึกษา ม.ปลาย",
                icon: "🌍",
                links: [
                    { title: "ภูมิศาสตร์อเมริกาเหนือ", url: "north-america-geography.html", type: "italic" }
                ]
            }
        ]
    }
];
