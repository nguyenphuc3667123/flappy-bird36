import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Cow - FlappyBird Style",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .main { background-color: #f1f2f6; }
        h1 { color: #2f3640; text-align: center; font-family: 'Segoe UI', sans-serif; font-size: 2rem; margin-bottom: 0px; }
        .instructions { text-align: center; color: #718093; font-size: 0.95rem; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐄 Flappy Cow Classic</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn phím <b>Space</b> hoặc <b>Click chuột</b> để điều khiển chú bò bay qua các ống nước!</div>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      display: flex;
      justify-content: center;
      background: transparent;
    }
    canvas {
      border: 3px solid #2f3640;
      background-color: #70c5ce;
      display: block;
      box-shadow: 0 8px 20px rgba(0,0,0,0.15);
      border-radius: 8px;
      outline: none;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="320" height="480" tabindex="1"></canvas>
  <script>
    const cvs = document.getElementById("gameCanvas");
    const ctx = cvs.getContext("2d");

    let cowX = 60, cowY = 200;
    let gravity = 0.22, velocity = 0, jump = -4.0;
    let score = 0, bestScore = 0;
    let isGameOver = false;
    let groundX = 0;
    let frameCount = 0;

    let pipes = [];
    pipes[0] = { x: cvs.width, topHeight: 140, gap: 120, passed: false };

    function resetGame() {
      if (score > bestScore) bestScore = score;
      cowY = 200;
      velocity = 0;
      score = 0;
      pipes = [{ x: cvs.width, topHeight: 140, gap: 120, passed: false }];
      isGameOver = false;
    }

    function handleInput(e) {
      if (e.code === "Space" || e.type === "click") {
        if (isGameOver) {
          resetGame();
        } else {
          velocity = jump;
        }
        if (e.code === "Space") e.preventDefault();
      }
    }

    window.addEventListener("keydown", handleInput);
    cvs.addEventListener("click", handleInput);
    cvs.focus();

    function drawCow(x, y, vel) {
      ctx.save();
      ctx.translate(x, y);
      let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, vel * 0.08));
      ctx.rotate(rotation);

      // Cánh vẫy
      let wingAngle = Math.sin(frameCount * 0.4) * 0.6;
      ctx.save();
      ctx.translate(-2, -9);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.ellipse(0, -6, 8, 4, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Thân bò
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#2f3640";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 17, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm thân
      ctx.fillStyle = "#2f3640";
      ctx.beginPath();
      ctx.arc(-4, -2, 5, 0, Math.PI * 2);
      ctx.arc(3, 3, 3, 0, Math.PI * 2);
      ctx.fill();

      // Đầu bò
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(13, -4, 8.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mõm hồng
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(18, -2, 4, 3, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mắt
      ctx.fillStyle = "#000";
      ctx.beginPath();
      ctx.arc(15, -7, 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Sừng
      ctx.fillStyle = "#dcdde1";
      ctx.beginPath();
      ctx.moveTo(10, -11);
      ctx.lineTo(13, -16);
      ctx.lineTo(16, -11);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function update() {
      frameCount++;

      // Nền trời xanh cổ điển
      ctx.fillStyle = "#70c5ce";
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Đám mây phong cách cổ điển đơn giản phía sau
      ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
      ctx.beginPath();
      ctx.arc(60, 100, 25, 0, Math.PI * 2);
      ctx.arc(85, 90, 20, 0, Math.PI * 2);
      ctx.arc(220, 160, 30, 0, Math.PI * 2);
      ctx.fill();

      if (!isGameOver) {
        velocity += gravity;
        cowY += velocity;

        // Cuộn mặt đất
        groundX -= 2;
        if (groundX <= -24) groundX = 0;

        // Xử lý ống
        for (let i = 0; i < pipes.length; i++) {
          // Ống màu xanh lá phong cách Flappy Bird gốc
          ctx.fillStyle = "#73bf2e";
          ctx.strokeStyle = "#558022";
          ctx.lineWidth = 2;

          let pipeWidth = 52;
          
          // Ống trên
          ctx.fillRect(pipes[i].x, 0, pipeWidth, pipes[i].topHeight);
          ctx.strokeRect(pipes[i].x, 0, pipeWidth, pipes[i].topHeight);
          // Đầu ống trên
          ctx.fillRect(pipes[i].x - 3, pipes[i].topHeight - 20, pipeWidth + 6, 20);
          ctx.strokeRect(pipes[i].x - 3, pipes[i].topHeight - 20, pipeWidth + 6, 20);

          // Ống dưới
          let botY = pipes[i].topHeight + pipes[i].gap;
          ctx.fillRect(pipes[i].x, botY, pipeWidth, cvs.height - 80 - botY);
          ctx.strokeRect(pipes[i].x, botY, pipeWidth, cvs.height - 80 - botY);
          // Đầu ống dưới
          ctx.fillRect(pipes[i].x - 3, botY, pipeWidth + 6, 20);
          ctx.strokeRect(pipes[i].x - 3, botY, pipeWidth + 6, 20);

          pipes[i].x -= 2;

          if (pipes[i].x === 130) {
            pipes.push({
              x: cvs.width,
              topHeight: Math.floor(Math.random() * 160) + 50,
              gap: 120,
              passed: false
            });
          }

          if (pipes[i].x < -60) pipes.shift();

          // Tính điểm
          if (!pipes[i].passed && pipes[i].x + pipeWidth < cowX) {
            score++;
            pipes[i].passed = true;
          }

          // Va chạm ống, đất hoặc bay quá cao
          if (
            cowX + 13 > pipes[i].x && cowX - 13 < pipes[i].x + pipeWidth &&
            (cowY - 11 < pipes[i].topHeight || cowY + 11 > botY) ||
            cowY + 12 >= cvs.height - 80 || cowY - 12 <= 0
          ) {
            isGameOver = true;
          }
        }
      }

      // Vẽ các cột ống và mặt đất
      // Vẽ mặt đất cuộn (Ground)
      ctx.fillStyle = "#ded895"; // Đất nền màu vàng cát
      ctx.fillRect(0, cvs.height - 80, cvs.width, 80);
      ctx.fillStyle = "#558022"; // Cỏ xanh phía trên mặt đất
      ctx.fillRect(0, cvs.height - 80, cvs.width, 16);

      // Đường sọc vằn chuyển động trên mặt đất
      ctx.fillStyle = "#d0342c";
      for (let g = groundX; g < cvs.width; g += 24) {
        ctx.beginPath();
        ctx.moveTo(g, cvs.height - 80);
        ctx.lineTo(g + 12, cvs.height - 80);
        ctx.lineTo(g + 4, cvs.height - 64);
        ctx.lineTo(g - 8, cvs.height - 64);
        ctx.fill();
      }

      drawCow(cowX, cowY, velocity);

      // Hiển thị điểm số ở giữa phía trên màn hình chuẩn phong cách Flappy Bird
      if (!isGameOver) {
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 4;
        ctx.font = "bold 35px Arial";
        ctx.textAlign = "center";
        ctx.strokeText(score, cvs.width / 2, 60);
        ctx.fillText(score, cvs.width / 2, 60);
      } else {
        // Bảng Game Over kiểu game thùng cổ điển
        ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        // Khung điểm (Score Board)
        ctx.fillStyle = "#ded895";
        ctx.strokeStyle = "#558022";
        ctx.lineWidth = 3;
        ctx.fillRect(60, 130, 200, 180);
        ctx.strokeRect(60, 130, 200, 180);

        ctx.fillStyle = "#b59e54";
        ctx.font = "bold 22px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", cvs.width / 2, 165);

        ctx.fillStyle = "#558022";
        ctx.font = "16px Arial";
        ctx.textAlign = "left";
        ctx.fillText("SCORE", 85, 205);
        ctx.fillText("BEST", 85, 250);

        ctx.textAlign = "right";
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px Arial";
        ctx.fillText(score, 235, 205);
        ctx.fillText(bestScore, 235, 250);

        // Hướng dẫn chơi lại
        ctx.textAlign = "center";
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 3;
        ctx.font = "bold 16px Arial";
        ctx.strokeText("Nhấn Space để chơi lại", cvs.width / 2, 350);
        ctx.fillText("Nhấn Space để chơi lại", cvs.width / 2, 350);
      }

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
"""

components.html(game_code, height=520)
