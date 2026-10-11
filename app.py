import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Flying Cow",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        h1 { color: #2c3e50; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 2.2rem; margin-bottom: 0px; }
        .instructions { text-align: center; color: #7f8c8d; font-size: 1rem; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐄 Flappy Flying Cow</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn <b>Space</b> hoặc <b>Click chuột</b> vào khung game để điều khiển chú bò bay thong thả!</div>", unsafe_allow_html=True)

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
      border: 4px solid #2c3e50;
      background: linear-gradient(to bottom, #3498db, #85c1e9);
      display: block;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      border-radius: 12px;
      outline: none;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="360" height="500" tabindex="1"></canvas>
  <script>
    const cvs = document.getElementById("gameCanvas");
    const ctx = cvs.getContext("2d");

    let cowX = 60, cowY = 220;
    let gravity = 0.15, velocity = 0, jump = -3.8; // Đã giảm trọng lực để bò rơi chậm hơn
    let score = 0, frameCount = 0;
    let isGameOver = false;

    let clouds = [
      { x: 40, y: 70, speed: 0.3 },
      { x: 200, y: 140, speed: 0.3 },
      { x: 330, y: 90, speed: 0.3 }
    ];

    let pipes = [{ x: 360, topHeight: 150, gap: 140 }];

    function resetGame() {
      cowY = 220;
      velocity = 0;
      score = 0;
      pipes = [{ x: 360, topHeight: 150, gap: 140 }];
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
      let rotation = Math.min(Math.PI / 5, Math.max(-Math.PI / 5, vel * 0.07));
      ctx.rotate(rotation);

      // Cánh vẫy
      let wingAngle = Math.sin(frameCount * 0.35) * 0.55;
      ctx.save();
      ctx.translate(-2, -10);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.ellipse(0, -7, 9, 4.5, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Thân bò
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#2c3e50";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 19, 13, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm thân
      ctx.fillStyle = "#2c3e50";
      ctx.beginPath();
      ctx.arc(-5, -3, 5.5, 0, Math.PI * 2);
      ctx.arc(3, 4, 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Đầu bò
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(15, -5, 9.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm đầu & Mõm
      ctx.fillStyle = "#2c3e50";
      ctx.beginPath();
      ctx.arc(17, -8, 2.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(21, -3, 4.5, 3.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mắt
      ctx.fillStyle = "#000";
      ctx.beginPath();
      ctx.arc(17, -9, 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Sừng
      ctx.fillStyle = "#bdc3c7";
      ctx.beginPath();
      ctx.moveTo(12, -13);
      ctx.lineTo(15, -18);
      ctx.lineTo(18, -13);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function update() {
      frameCount++;
      
      let grad = ctx.createLinearGradient(0, 0, 0, cvs.height);
      grad.addColorStop(0, "#2980b9");
      grad.addColorStop(1, "#6dd5fa");
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      ctx.fillStyle = "rgba(255, 255, 255, 0.65)";
      for (let c of clouds) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, 18, 0, Math.PI * 2);
        ctx.arc(c.x + 10, c.y - 7, 13, 0, Math.PI * 2);
        ctx.arc(c.x + 20, c.y, 15, 0, Math.PI * 2);
        ctx.fill();
        c.x -= c.speed;
        if (c.x < -40) c.x = cvs.width + 40;
      }

      if (!isGameOver) {
        velocity += gravity;
        cowY += velocity;

        for (let i = 0; i < pipes.length; i++) {
          let pColor = "#27ae60", pBorder = "#1e8449";
          ctx.fillStyle = pColor;
          ctx.strokeStyle = pBorder;
          ctx.lineWidth = 2;

          ctx.fillRect(pipes[i].x, 0, 48, pipes[i].topHeight);
          ctx.strokeRect(pipes[i].x, 0, 48, pipes[i].topHeight);
          ctx.fillRect(pipes[i].x - 3, pipes[i].topHeight - 18, 54, 18);
          ctx.strokeRect(pipes[i].x - 3, pipes[i].topHeight - 18, 54, 18);

          let botY = pipes[i].topHeight + pipes[i].gap;
          ctx.fillRect(pipes[i].x, botY, 48, cvs.height - botY);
          ctx.strokeRect(pipes[i].x, botY, 48, cvs.height - botY);
          ctx.fillRect(pipes[i].x - 3, botY, 54, 18);
          ctx.strokeRect(pipes[i].x - 3, botY, 54, 18);

          pipes[i].x -= 2.0; // Giảm tốc độ ống chạy một chút cho đồng bộ

          if (pipes[i].x === 140) {
            pipes.push({
              x: cvs.width,
              topHeight: Math.floor(Math.random() * 190) + 60,
              gap: 140
            });
          }

          if (pipes[i].x < -60) pipes.shift();

          if (
            cowX + 15 > pipes[i].x && cowX - 15 < pipes[i].x + 48 &&
            (cowY - 11 < pipes[i].topHeight || cowY + 11 > botY) ||
            cowY + 13 > cvs.height || cowY - 13 < 0
          ) {
            isGameOver = true;
          }

          if (Math.abs(pipes[i].x - cowX) < 1.0) score++;
        }
      }

      drawCow(cowX, cowY, velocity);

      if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 26px Segoe UI";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", cvs.width / 2, cvs.height / 2 - 20);
        
        ctx.font = "16px Segoe UI";
        ctx.fillText("Điểm của bạn: " + score, cvs.width / 2, cvs.height / 2 + 15);
        ctx.fillText("Nhấn Space / Click để chơi lại", cvs.width / 2, cvs.height / 2 + 50);
        ctx.textAlign = "left";
      } else {
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 3;
        ctx.font = "bold 24px Segoe UI";
        ctx.strokeText("Score: " + score, 20, 35);
        ctx.fillText("Score: " + score, 20, 35);
      }

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
"""

components.html(game_code, height=520)
