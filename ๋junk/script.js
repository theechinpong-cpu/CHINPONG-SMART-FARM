const questions = [
    { q: "1. 25 x 4 เท่ากับเท่าไหร่?", options: ["80", "90", "100", "110"], answer: 2 },
    { q: "2. ห.ร.ม. ของ 12 และ 18 คืออะไร?", options: ["2", "3", "6", "9"], answer: 2 }
];

const container = document.getElementById('quiz-container');

questions.forEach((item, index) => {
    let html = `<div class="mb-6 p-4 border rounded-lg shadow-sm bg-white">
        <p class="font-semibold mb-3 text-lg">${item.q}</p>`;
    item.options.forEach((opt, i) => {
        html += `<label class="block mb-2 cursor-pointer hover:bg-blue-50 p-2 rounded">
            <input type="radio" name="q${index}" value="${i}" class="mr-2"> ${opt}
        </label>`;
    });
    html += `</div>`;
    container.innerHTML += html;
});

async function submitExam() {
    let score = 0;
    let studentName = "นักเรียนทดสอบ"; // ในอนาคตจะดึงจาก Google Login

    questions.forEach((item, index) => {
        const selected = document.querySelector(`input[name="q${index}"]:checked`);
        if (selected && parseInt(selected.value) === item.answer) {
            score++;
        }
    });

    alert(`บันทึกคำตอบเรียบร้อย! คุณได้คะแนน ${score} / ${questions.length}`);
    
    // ส่งข้อมูลเข้า LINE (ผ่านระบบ Notify หรือ API ที่คุณตั้งค่าไว้)
    await sendToLine(studentName, score);
}

async function sendToLine(name, score) {
    const message = `📢 รายงานผลสอบ: ${name}\nวิชา: คณิตศาสตร์ ป.6\nคะแนนที่ได้: ${score}/${questions.length} ข้อ`;
    
    console.log("ส่งข้อมูลไป LINE:", message);
    // หมายเหตุ: การเชื่อมต่อ LINE API จริงต้องใช้ไฟล์หลังบ้าน (Serverless Function) 
    // เพื่อความปลอดภัยของ Token ซึ่ง Vercel รองรับครับ
}
