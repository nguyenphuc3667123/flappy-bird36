import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Detailed Flying Cow Game", layout="centered")

st.title("🐄 Flappy Flying Cow - Bản Chi Tiết")
st.write("Dùng phím **Space** hoặc **Click chuột** để điều khiển chú bò bay lượn giữa các đám mây!")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    canvas {
      border: 3px solid #333;
      background: linear-gradient(to bottom, #4a90e2, #87ceeb);
      display: block;
      margin: 0 auto;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <canvas id="canvas" width="350" height="500"></canvas>
  <script>
    const cvs = document.getElementById("canvas");
    const ctx = cvs.getContext("2d");

    let cowX = 60;
    let cowY = 200;
    let gravity = 0.22;
    let velocity = 0;
    let jump = -4.2;
    let score = 0;
    let frameCount = 0;

    // Danh sách mây nền
    let clouds = [
      { x: 50, y: 80, speed: 0.5 },
      { x: 220, y: 150, speed: 0.5 },
      { x: 320, y: 60, speed: 0.5 }
    ];

    let pipes = [];
    pipes[0] = { x: cvs.width, topHeight: 160, gap: 130 };

    document.addEventListener("keydown", function(e) {
      if (e.code === "Space") {
        velocity = jump;
        e.preventDefault(); // Ngăn trình duyệt cuộn trang
      }
    });
    
    cvs.addEventListener("click", function() {
      velocity = jump;
    });

    function drawCow(x, y, vel) {
      ctx.save();
      ctx.translate(x, y);

      // Xoay nhẹ chú bò theo hướng bay lên/rơi xuống
      let rotation = Math.min(Math.PI / 6, Math.max(-Math.PI / 6, vel * 0.08));
      ctx.rotate(rotation);

      // Cánh vẫy (động tác dựa vào frameCount)
      let wingAngle = Math.sin(frameCount * 0.3) * 0.5;
      ctx.save();
      ctx.translate(-2, -10);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#444";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.ellipse(0, -8, 10, 5, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Thân bò (Hình bầu dục trắng)
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 20, 14, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Các đốm đen trên thân
      ctx.fillStyle = "#222222";
      ctx.beginPath();
      ctx.arc(-6, -4, 6, 0, Math.PI * 2);
      ctx.arc(4, 5, 4, 0, Math.PI * 2);
      ctx.fill();

      // Đầu bò
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(16, -5, 10, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm trên mặt
      ctx.fillStyle = "#222222";
      ctx.beginPath();
      ctx.arc(18, -8, 3, 0, Math.PI * 2);
      ctx.fill();

      // Mõm bò hồng phớt
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(22, -3, 5, 4, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mũi (2 lỗ mũi nhỏ)
      ctx.fillStyle = "#a0522d";
      ctx.beginPath();
      ctx.arc(20, -4, 1, 0, Math.PI * 2);
      ctx.arc(23, -4, 1, 0, Math.PI * 2);
      ctx.fill();

      // Mắt bò
      ctx.fillStyle = "#000000";
      ctx.beginPath();
      ctx.arc(18, -9, 1.5, 0, Math.PI * 2);
      ctx.fill();

      // Sừng bò màu xám chi tiết
      ctx.fillStyle = "#d3d3d3";
      ctx.beginPath();
      ctx.moveTo(13, -13);
      ctx.lineTo(16, -19);
      ctx.lineTo(19, -14);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function draw() {
      frameCount++;

      // Xóa màn hình với màu nền trời chuyển sắc
      let gradient = ctx.createLinearGradient(0, 0, 0, cvs.height);
      gradient.addColorStop(0, "#4a90e2");
      gradient.addColorStop(1, "#a1c4fd");
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Vẽ mây trôi ở background
      ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
      for (let c of clouds) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, 20, 0, Math.PI * 2);
        ctx.arc(c.x + 12, c.y - 8, 15, 0, Math.PI * 2);
        ctx.arc(c.x + 22, c.y, 18, 0, Math.PI * 2);
        ctx.fill();

        c.x -= c.speed;
        if (c.x < -40) c.x = cvs.width + 40;
      }

      // Cập nhật lý tính chú bò
      velocity += gravity;
      cowY += velocity;

      // Vẽ chú bò
      drawCow(cowX, cowY, velocity);

      // Xử lý hệ thống ống cản (pipes)
      for (let i = 0; i < pipes.length; i++) {
        // Thiết kế ống có viền và hiệu ứng trụ
        let pipeColor = "#27ae60";
        let pipeBorder = "#1e8449";
        
        ctx.fillStyle = pipeColor;
        ctx.strokeStyle = pipeBorder;
        ctx.lineWidth = 2;

        // Ống trên
        ctx.fillRect(pipes[i].x, 0, 50, pipes[i].topHeight);
        ctx.strokeRect(pipes[i].x, 0, 50, pipes[i].topHeight);
        // Miệng ống trên
        ctx.fillRect(pipes[i].x - 3, pipes[i].topHeight - 20, 56, 20);
        ctx.strokeRect(pipes[i].x - 3, pipes[i].topHeight - 20, 56, 20);

        // Ống dưới
        let bottomPipeY = pipes[i].topHeight + pipes[i].gap;
        ctx.fillRect(pipes[i].x, bottomPipeY, 50, cvs.height - bottomPipeY);
        ctx.strokeRect(pipes[i].x, bottomPipeY, 50, cvs.height - bottomPipeY);
        // Miệng ống dưới
        ctx.fillRect(pipes[i].x - 3, bottomPipeY, 56, 20);
        ctx.strokeRect(pipes[i].x - 3, bottomPipeY, 56, 20);

        pipes[i].x -= 2.2;

        // Tạo ống mới khi ống cũ di chuyển vào giữa màn hình
        if (pipes[i].x === 130) {
          pipes.push({
            x: cvs.width,
            topHeight: Math.floor(Math.random() * 200) + 60,
            gap: 130
          });
        }

        // Xóa ống cũ đã đi ra ngoài màn hình để tối ưu bộ nhớ
        if (pipes[i].x < -60) {
          pipes.shift();
        }

        // Kiểm tra va chạm chi tiết với thân bò
        if (
          cowX + 16 > pipes[i].x && cowX - 16 < pipes[i].x + 50 &&
          (cowY - 12 < pipes[i].topHeight || cowY + 12 > pipes[i].topHeight + pipes[i].gap) ||
          cowY + 14 > cvs.height || cowY - 14 < 0
        ) {
          location.reload(); // Thua thì làm lại
        }

        // Tính điểm khi vượt qua ống
        if (Math.abs(pipes[i].x - cowX) < 1.1) {
          score++;
        }
      }

      // Hiển thị điểm số phong cách nổi bật
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#000000";
      ctx.lineWidth = 4;
      ctx.font = "bold 28px Arial";
      ctx.strokeText("Score: " + score, 20, 40);
      ctx.fillText("Score: " + score, 20, 40);

      requestAnimationFrame(draw);
    }

    draw();
  </script>
</body>
</html>
"""

components.html(game_code, height=540)
