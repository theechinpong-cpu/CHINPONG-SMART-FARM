const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors()); // อนุญาตให้ทุก Domain เข้าถึงได้

const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*", // สำคัญมาก: เพื่อให้มือถือและ Dashboard คุยกันได้
        methods: ["GET", "POST"]
    }
});

let scores = { 
    player1: { name: "Player 1", score: 0 }, 
    player2: { name: "Player 2", score: 0 } 
};

io.on('connection', (socket) => {
    console.log('A user connected: ' + socket.id);

    // ส่งคะแนนปัจจุบันให้คนที่เพิ่งเปิดหน้าจอ (เช่น Dashboard)
    socket.emit('update-dashboard', scores);

    // รับคะแนนจากมือถือเด็ก
    socket.on('submit-score', (data) => {
        console.log('Score received:', data);
        if (data.player === 1) scores.player1.score += data.points;
        if (data.player === 2) scores.player2.score += data.points;
        
        // Broadcast อัปเดตให้ทุกหน้าจอ (รวมถึง Dashboard) ทันที
        io.emit('update-dashboard', scores);
    });

    socket.on('reset-game', () => {
        scores.player1.score = 0;
        scores.player2.score = 0;
        io.emit('update-dashboard', scores);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
