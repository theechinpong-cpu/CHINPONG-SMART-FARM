const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

let scores = { player1: { name: "Player 1", score: 0 }, player2: { name: "Player 2", score: 0 } };

io.on('connection', (socket) => {
    // ส่งคะแนนปัจจุบันให้คนที่เพิ่ง Connect (เช่น Dashboard)
    socket.emit('update-dashboard', scores);

    // รับคะแนนจากมือถือเด็ก
    socket.on('submit-score', (data) => {
        if (data.player === 1) scores.player1.score += data.points;
        if (data.player === 2) scores.player2.score += data.points;
        
        // ส่งคะแนนที่อัปเดตไปให้ Dashboard ทันที
        io.emit('update-dashboard', scores);
    });

    socket.on('reset-game', () => {
        scores.player1.score = 0;
        scores.player2.score = 0;
        io.emit('update-dashboard', scores);
    });
});

server.listen(3000, () => console.log('Server running on port 3000'));
