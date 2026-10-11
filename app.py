<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird - GitHub Edition</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
        }
        body {
            margin: 0;
            padding: 0;
            background: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-radius: 10px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #70c5ce;
        }
        .instructions {
            position: absolute;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: white;
            font-size: 14px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            pointer-events: none;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="400" height="600"></canvas>
    <div class="instructions">Nhấn Phím Cách (Space) hoặc Chạm màn hình để bay</div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Thông số game
    let frames = 0;
    const DEGREE = Math.PI / 180;

    // Trạng thái game
    const state = {
        current: 0,
        getReady: 0,
        game: 1,
        over: 2
    };

    // Điều khiển
    document.addEventListener("keydown", function(e) {
        if (e.code === "Space" || e.code === "ArrowUp") {
            handleAction();
        }
    });

    canvas.addEventListener("click", function() {
        handleAction();
    });

    canvas.addEventListener("touchstart", function(e) {
        e.preventDefault();
        handleAction();
    }, { passive: false });

    function handleAction() {
        switch (state.current) {
            case state.getReady:
                state.current = state.game;
                bird.flap();
                break;
            case state.game:
                bird.flap();
                break;
            case state.over:
                // Kiểm tra click vào nút chơi lại
                if (bird.speed === 0) { // Đảm bảo bird đã rơi xuống đất xong hoặc sau khi game over ngắn
                    resetGame();
                }
                break;
        }
    }

    function resetGame() {
        pipes.reset();
        bird.speed = 0;
        bird.y = 150;
        bird.rotation = 0;
        score.value = 0;
        state.current = state.getReady;
    }

    // Đối tượng Chú Chim
    const bird = {
        x: 50,
        y: 150,
        w: 34,
        h: 24,
        radius: 12,
        gravity: 0.25,
        jump: 4.6,
        speed: 0,
        rotation: 0,

        draw: function() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation);

            // Vẽ thân chim (Màu vàng)
            ctx.fillStyle = "#f8e71c";
            ctx.beginPath();
            ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#000";
            ctx.stroke();

            // Vẽ cánh (Màu trắng/cam)
            ctx.fillStyle = "#f5a623";
            ctx.beginPath();
            ctx.ellipse(-3, 2, 8, 5, Math.PI / 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            // Vẽ mắt
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(6, -4, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = "#000";
            ctx.beginPath();
            ctx.arc(8, -4, 2, 0, Math.PI * 2);
            ctx.fill();

            // Vẽ mỏ
            ctx.fillStyle = "#f5a623";
            ctx.beginPath();
            ctx.moveTo(10, -1);
            ctx.lineTo(20, 3);
            ctx.lineTo(10, 7);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            ctx.restore();
        },

        flap: function() {
            this.speed = -this.jump;
        },

        update: function() {
            // Nếu ở màn hình Get Ready, chim bay lên xuống nhẹ nhàng
            if (state.current === state.getReady) {
                this.y = 150 + Math.sin(frames * 0.1) * 5;
                this.rotation = 0;
            } else {
                this.speed += this.gravity;
                this.y += this.speed;

                // Kiểm tra va chạm đất
                if (this.y + this.h / 2 >= canvas.height - 100) {
                    this.y = canvas.height - 100 - this.h / 2;
                    if (state.current === state.game) {
                        state.current = state.over;
                    }
                }

                // Giới hạn đầu chim không bay vượt quá màn hình
                if (this.y - this.h / 2 <= 0) {
                    this.y = this.h / 2;
                    this.speed = 0;
                }

                // Góc quay của chim theo vận tốc
                if (this.speed >= this.jump) {
                    this.rotation = 90 * DEGREE;
                    if (this.y >= canvas.height - 100) {
                        this.speed = 0; // Dừng khi chạm đất
                    }
                } else {
                    this.rotation = -25 * DEGREE;
                }
            }
        }
    };

    // Đối tượng Ống nước
    const pipes = {
        position: [],
        top: 240,
        bottom: 240,
        w: 53,
        h: 400,
        gap: 110,
        dx: 2,

        draw: function() {
            for (let i = 0; i < this.position.length; i++) {
                let p = this.position[i];
                let topYPos = p.y;
                let bottomYPos = p.y + this.h + this.gap;

                // Ống trên
                ctx.fillStyle = "#73bf2e";
                ctx.fillRect(p.x, topYPos, this.w, this.h);
                ctx.lineWidth = 2;
                ctx.strokeStyle = "#2e5e14";
                ctx.strokeRect(p.x, topYPos, this.w, this.h);
                // Đầu ống trên
                ctx.fillRect(p.x - 3, topYPos + this.h - 20, this.w + 6, 20);
                ctx.strokeRect(p.x - 3, topYPos + this.h - 20, this.w + 6, 20);

                // Ống dưới
                ctx.fillRect(p.x, bottomYPos, this.w, this.h);
                ctx.strokeRect(p.x, bottomYPos, this.w, this.h);
                // Đầu ống dưới
                ctx.fillRect(p.x - 3, bottomYPos, this.w + 6, 20);
                ctx.strokeRect(p.x - 3, bottomYPos, this.w + 6, 20);
            }
        },

        update: function() {
            if (state.current !== state.game) return;

            if (frames % 100 === 0) {
                this.position.push({
                    x: canvas.width,
                    y: -Math.floor(Math.random() * 180) - 100
                });
            }

            for (let i = 0; i < this.position.length; i++) {
                let p = this.position[i];
                p.x -= this.dx;

                // Kiểm tra va chạm chim với ống
                let bottomYPos = p.y + this.h + this.gap;

                // Va chạm ống trên
                if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                    bird.y - bird.radius < p.y + this.h) {
                    state.current = state.over;
                }
                // Va chạm ống dưới
                if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                    bird.y + bird.radius > bottomYPos) {
                    state.current = state.over;
                }

                // Xóa ống khi ra ngoài màn hình
                if (p.x + this.w <= 0) {
                    this.position.shift();
                    score.value++;
                    score.best = Math.max(score.value, score.best);
                    localStorage.setItem("bestScore", score.best);
                }
            }
        },

        reset: function() {
            this.position = [];
        }
    };

    // Đối tượng Điểm số
    const score = {
        value: 0,
        best: parseInt(localStorage.getItem("bestScore")) || 0,

        draw: function() {
            ctx.fillStyle = "#FFF";
            ctx.strokeStyle = "#000";

            if (state.current === state.game) {
                ctx.lineWidth = 2;
                ctx.font = "35px Arial";
                ctx.textAlign = "center";
                ctx.fillText(this.value, canvas.width / 2, 50);
                ctx.strokeText(this.value, canvas.width / 2, 50);
            } else if (state.current === state.over) {
                // Bảng điểm Game Over
                ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#FFF";
                ctx.font = "bold 35px Arial";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width / 2, 180);

                // Khung điểm
                ctx.fillStyle = "#ded895";
                ctx.fillRect(canvas.width / 2 - 130, 210, 260, 130);
                ctx.lineWidth = 3;
                ctx.strokeStyle = "#555";
                ctx.strokeRect(canvas.width / 2 - 130, 210, 260, 130);

                ctx.fillStyle = "#715531";
                ctx.font = "20px Arial";
                ctx.textAlign = "left";
                ctx.fillText("Điểm", canvas.width / 2 - 100, 255);
                ctx.fillText("Cao nhất", canvas.width / 2 - 100, 305);

                ctx.font = "bold 22px Arial";
                ctx.textAlign = "right";
                ctx.fillText(this.value, canvas.width / 2 + 100, 255);
                ctx.fillText(this.best, canvas.width / 2 + 100, 305);

                // Nút chơi lại
                ctx.fillStyle = "#f5a623";
                ctx.fillRect(canvas.width / 2 - 80, 370, 160, 45);
                ctx.strokeRect(canvas.width / 2 - 80, 370, 160, 45);

                ctx.fillStyle = "#FFF";
                ctx.font = "bold 20px Arial";
                ctx.textAlign = "center";
                ctx.fillText("CHƠI LẠI", canvas.width / 2, 400);
            } else if (state.current === state.getReady) {
                ctx.lineWidth = 2;
                ctx.font = "bold 30px Arial";
                ctx.textAlign = "center";
                ctx.fillText("Đ SH SẴN SÀNG", canvas.width / 2, 180); // Hoặc "SẴN SÀNG"
                ctx.fillStyle = "#FFF";
                ctx.fillText("SẴN SÀNG", canvas.width / 2, 180);
                ctx.strokeText("SẴN SÀNG", canvas.width / 2, 180);
            }
        }
    };

    // Vẽ Nền và Mặt đất
    function drawBackground() {
        // Màu trời (Canvas background đã tạo sẵn)

        // Vẽ mây
        ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
        ctx.beginPath();
        ctx.arc(80, 100, 30, 0, Math.PI * 2);
        ctx.arc(110, 90, 40, 0, Math.PI * 2);
        ctx.arc(140, 105, 25, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(280, 200, 25, 0, Math.PI * 2);
        ctx.arc(310, 190, 35, 0, Math.PI * 2);
        ctx.arc(335, 205, 20, 0, Math.PI * 2);
        ctx.fill();
    }

    const foreground = {
        h: 100,
        draw: function() {
            // Lớp đất cỏ trên cùng
            ctx.fillStyle = "#73bf2e";
            ctx.fillRect(0, canvas.height - this.h, canvas.width, 20);
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#2e5e14";
            ctx.strokeRect(0, canvas.height - this.h, canvas.width, 2
