// menu.js - Full Curriculum Structure 2026
const lessonMenu = [
    {
        category: "Primary Level (ป.1 - ป.6)",
        color: "green",
        icon: "fas fa-pencil-alt",
        items: [
            {
                subject: "Mathematics", icon: "🔢",
                links: [
                    { title: "จำนวนและพีชคณิต", url: "math-p-algebra.html", type: "bold" },
                    { title: "เรขาคณิตและสถิติ", url: "math-p-geo.html", type: "normal" }
                ]
            },
            {
                subject: "Science & Tech", icon: "🧪",
                links: [
                    { title: "วิทยาศาสตร์กายภาพ", url: "sci-p-phys.html", type: "normal" },
                    { title: "วิทยาการคำนวณ (Coding)", url: "sci-p-coding.html", type: "bold" }
                ]
            }
        ]
    },
    {
        category: "Secondary Level (ม.1 - ม.6)",
        color: "rose",
        icon: "fas fa-university",
        items: [
            {
                subject: "Pure Sciences", icon: "🧬",
                links: [
                    { title: "ฟิสิกส์ (Physics)", url: "phys-m-all.html", type: "normal" },
                    { title: "ชีววิทยา (Biology)", url: "bio-m-all.html", type: "bold" },
                    { title: "เคมี (Chemistry)", url: "chem-m-all.html", type: "normal" }
                ]
            },
            {
                subject: "English Specials", icon: "👨‍🍳",
                links: [
                    { title: "Culinary English (Chef)", url: "en-m4-chef.html", type: "bold" },
                    { title: "English for Academic", url: "en-m-academic.html", type: "italic" }
                ]
            },
            {
                subject: "Social & Geography", icon: "🌍",
                links: [
                    { title: "ภูมิศาสตร์อเมริกาเหนือ", url: "soc-m6-america.html", type: "normal" },
                    { title: "ประวัติศาสตร์โลก", url: "his-m-world.html", type: "normal" }
                ]
            }
        ]
    }
];
