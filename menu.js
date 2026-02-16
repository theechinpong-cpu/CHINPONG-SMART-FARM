const lessonMenu = [
    {
        category: "ระดับประถม (ป.1 - ป.6)",
        color: "green",
        icon: "fas fa-child",
        items: [
            { subject: "วิชาหลัก (สพฐ.)", icon: "📚", links: [
                { title: "ภาษาไทย/วรรณคดี", url: "th-p-all.html", type: "normal" },
                { title: "คณิตศาสตร์พื้นฐาน", url: "math-p-base.html", type: "normal" },
                { title: "วิทยาศาสตร์/Coding", url: "sci-p-base.html", type: "bold" },
                { title: "สังคม/ประวัติ/ศาสนา", url: "soc-p-all.html", type: "normal" },
                { title: "ภาษาอังกฤษพื้นฐาน", url: "en-p-base.html", type: "bold" }
            ]},
            { subject: "ทักษะชีวิตและวิชาเลือก", icon: "🎨", links: [
                { title: "การงานอาชีพ/ศิลปะ/ดนตรี", url: "life-skill-p.html", type: "normal" },
                { title: "สุขศึกษาและพลศึกษา", url: "health-p.html", type: "normal" },
                { title: "หน้าที่พลเมือง/ต้านทุจริต", url: "civic-p.html", type: "italic" }
            ]},
            { subject: "ศูนย์ติวสอบเข้า ม.1", icon: "🎯", links: [
                { title: "เจาะลึกโจทย์คณิต (Gifted)", url: "math-m1-entry.html", type: "bold" },
                { title: "ภาษาอังกฤษ (Pre-Test)", url: "en-m1-entry.html", type: "bold" }
            ]}
        ]
    },
    {
        category: "ระดับมัธยม (ม.1 - ม.6)",
        color: "rose",
        icon: "fas fa-university",
        items: [
            { subject: "สายวิทย์-คณิต (ม.ปลาย)", icon: "🔬", links: [
                { title: "ฟิสิกส์ (ครบทุกบท)", url: "phys-main.html", type: "normal" },
                { title: "เคมี (ครบทุกบท)", url: "chem-main.html", type: "normal" },
                { title: "ชีววิทยา (ครบทุกบท)", url: "bio-main.html", type: "bold" }
            ]},
            { subject: "แนวข้อสอบ ม.4 สายศิลป์ (17 ก.พ. 69)", icon: "✍️", links: [
                { title: "แนวข้อสอบวิชาภาษาอังกฤษ ปลายภาค", url: "en-m4-final.html", type: "bold" },
                { title: "มหาเวสสันดรชาดก", url: "th-m4-ves.html", type: "normal" },
                { title: "มงคลสูตรคำฉันท์", url: "th-m4-monkol.html", type: "normal" },
                { title: "การฟัง การดู และการพูดในโอกาสต่าง ๆ", url: "th-m4-speech.html", type: "normal" },
                { title: "การแต่งอินทรวิเชียรฉันท์", url: "th-m4-chan.html", type: "italic" }
            ]},
            { subject: "สายศิลป์และภาษา", icon: "👩‍🍳", links: [
                { title: "Culinary English (Chef)", url: "en-m4-chef.html", type: "bold" },
                { title: "ภาษาไทย/สังคม ม.ปลาย", url: "th-soc-m-high.html", type: "normal" },
                { title: "ภูมิศาสตร์อเมริกาเหนือ", url: "soc-m6-america.html", type: "italic" }
            ]},
            { subject: "คลังข้อสอบ TCAS / TGAT / TPAT", icon: "📝", links: [
                { title: "แนวข้อสอบวิชาภาษาอังกฤษ ม.4 ปลายภาค", url: "m4-english-final.html", type: "bold" },
                { title: "แนวข้อสอบวิชาภาษาไทย ม.4 ปลายภาค", url: "Thai-Final-Guideline.html", type: "bold" },
                { title: "ติวสอบ TGAT (ทุกพาร์ท)", url: "tgas-all.html", type: "bold" },
                { title: "แนวข้อสอบ A-Level", url: "alevel-all.html", type: "bold" }
            ]}
        ]
    }
];
