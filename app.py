import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Flying Cow - Large Edition",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        h1 { color: #1e3799; text-align: center; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 2.4rem; margin-bottom: 0px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
        .instructions { text-align: center; color: #485460; font-size: 1.1rem; margin-bottom: 15px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐄 Flappy Flying Cow (Bản Phóng To)</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn phím <b>Space</b> hoặc <b>Click chuột</b> vào khung game để điều khiển chú bò bay!</div>", unsafe_allow_html=True)

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
      border: 4px solid #1e3799;
      background: linear-gradient(to bottom, #4a69bd, #6a89cc, #786fa6);
      display: block;
      box-shadow: 0 14px 35px rgba(0,0,0,0.3);
      border-radius: 14px;
      outline: none;
    }
  </style>
</head>
<body>
  <!-- Phóng to màn hình canvas lên 400x600 -->
  <canvas id="gameCanvas" width="400" height="600" tabindex="1"></canvas>
  <script>
    const cvs = document.getElementById("gameCanvas");
    const ctx = cvs.getContext("2d");

    let cowX = 90, cowY = 260;
    let gravity = 0.15, velocity = 0, jump = -3.9;
    let score = 0, bestScore = 0;
    let gameState = "START"; // START, PLAYING, GAMEOVER
    let groundX = 0;
    let frameCount = 0;

    let clouds = [
      { x: 60, y: 100, speed: 0.3, size: 30 },
      { x: 250, y: 180, speed: 0.3, size: 24 },
      { x: 360, y: 80, speed: 0.3, size: 35 }
    ];

    let pipes = [];

    function initGame() {
      cowY = 260;
      velocity = 0;
      score = 0;
      pipes = [{ x: cvs.width, topHeight: 180, gap: 150, passed: false }];
    }

    function handleInput(e) {
      if (e.code === "Space" || e.type === "click") {
        if (gameState === "START") {
          gameState = "PLAYING";
          initGame();
          velocity = jump;
        } else if (gameState === "PLAYING") {
          velocity = jump;
        } else if (gameState === "GAMEOVER") {
          if (score > bestScore) bestScore = score;
          gameState = "PLAYING";
          initGame();
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

      // Phóng to kích thước chú bò cho cân đối màn hình
      ctx.scale(1.3, 1.3);

      // Cánh vẫy
      let wingAngle = Math.sin(frameCount * 0.35) * 0.55;
      ctx.save();
      ctx.translate(-2, -9);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#2f3640";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.ellipse(0, -6, 9, 4.5, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Thân bò
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#1e272c";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 18, 13, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm bò
      ctx.fillStyle = "#1e272c";
      ctx.beginPath();
      ctx.arc(-4, -2, 5.5, 0, Math.PI * 2);
      ctx.arc(3, 4, 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Đầu bò
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(14, -4, 9, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Má hồng
      ctx.fillStyle = "rgba(255, 107, 129, 0.4)";
      ctx.beginPath();
      ctx.arc(17, 0, 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Mõm hồng
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(19, -2, 4.5, 3.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mắt
      ctx.fillStyle = "#000";
      ctx.beginPath();
      ctx.arc(16, -7, 1.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#fff";
      ctx.beginPath();
      ctx.arc(16.5, -7.5, 0.4, 0, Math.PI * 2);
      ctx.fill();

      // Sừng
      ctx.fillStyle = "#dcdde1";
      ctx.strokeStyle = "#1e272c";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(11, -12);
      ctx.lineTo(14, -17);
      ctx.lineTo(17, -12);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function update() {
      frameCount++;

      // Nền trời
      let bgGrad = ctx.createLinearGradient(0, 0, 0, cvs.height);
      bgGrad.addColorStop(0, "#4a69bd");
      bgGrad.addColorStop(0.5, "#6a89cc");
      bgGrad.addColorStop(1, "#82ccdd");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Mây trôi
      ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
      for (let c of clouds) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.size, 0, Math.PI * 2);
        ctx.arc(c.x + c.size * 0.6, c.y - c.size * 0.3, c.size * 0.7, 0, Math.PI * 2);
        ctx.arc(c.x + c.size * 1.2, c.y, c.size * 0.8, 0, Math.PI * 2);
        ctx.fill();
        c.x -= c.speed;
        if (c.x < -80) c.x = cvs.width + 80;
      }

      let groundHeight = 95;

      if (gameState === "PLAYING") {
        velocity += gravity;
        cowY += velocity;

        groundX -= 2.0;
        if (groundX <= -32) groundX = 0;

        // Xử lý ống
        for (let i = 0; i < pipes.length; i++) {
          let pWidth = 64; // Tăng độ rộng ống cho tương xứng màn hình to
          let pipeGrad = ctx.createLinearGradient(pipes[i].x, 0, pipes[i].x + pWidth, 0);
          pipeGrad.addColorStop(0, "#2ecc71");
          pipeGrad.addColorStop(0.5, "#27ae60");
          pipeGrad.addColorStop(1, "#1e8449");

          ctx.fillStyle = pipeGrad;
          ctx.strokeStyle = "#145a32";
          ctx.lineWidth = 2;

          // Ống trên
          ctx.fillRect(pipes[i].x, 0, pWidth, pipes[i].topHeight);
          ctx.strokeRect(pipes[i].x, 0, pWidth, pipes[i].topHeight);
          ctx.fillRect(pipes[i].x - 5, pipes[i].topHeight - 25, pWidth + 10, 25);
          ctx.strokeRect(pipes[i].x - 5, pipes[i].topHeight - 25, pWidth + 10, 25);

          // Ống dưới
          let botY = pipes[i].topHeight + pipes[i].gap;
          ctx.fillRect(pipes[i].x, botY, pWidth, cvs.height - groundHeight - botY);
          ctx.strokeRect(pipes[i].x, botY, pWidth, cvs.height - groundHeight - botY);
          ctx.fillRect(pipes[i].x - 5, botY, pWidth + 10, 25);
          ctx.strokeRect(pipes[i].x - 5, botY, pWidth + 10, 25);

          pipes[i].x -= 2.0;

          if (pipes[i].x === 160) {
            pipes.push({
              x: cvs.width,
              topHeight: Math.floor(Math.random() * 220) + 70,
              gap: 150,
              passed: false
            });
          }

          if (pipes[i].x < -80) pipes.shift();

          if (!pipes[i].passed && pipes[i].x + pWidth < cowX) {
            score++;
            pipes[i].passed = true;
          }

          // Kiểm tra va chạm (tính theo hitbox chú bò phóng to)
          let cowRadius = 18;
          if (
            cowX + cowRadius > pipes[i].x && cowX - cowRadius < pipes[i].x + pWidth &&
            (cowY - cowRadius < pipes[i].topHeight || cowY + cowRadius > botY) ||
            cowY + cowRadius >= cvs.height - groundHeight || cowY - cowRadius <= 0
          ) {
            gameState = "GAMEOVER";
          }
        }
      }

      // Vẽ mặt đất lớn hơn
      let groundY = cvs.height - groundHeight;
      ctx.fillStyle = "#f1c40f";
      ctx.fillRect(0, groundY, cvs.width, groundHeight);
      ctx.fillStyle = "#27ae60";
      ctx.fillRect(0, groundY, cvs.width, 20);

      ctx.fillStyle = "#d35400";
      for (let g = groundX; g < cvs.width; g += 32) {
        ctx.beginPath();
        ctx.moveTo(g, groundY);
        ctx.lineTo(g + 16, groundY);
        ctx.lineTo(g + 6, groundY + 20);
        ctx.lineTo(g - 10, groundY + 20);
        ctx.fill();
      }

      // Vẽ chú bò
      if (gameState === "START") {
        let hoverY = 260 + Math.sin(frameCount * 0.08) * 10;
        drawCow(cowX, hoverY, 0);
      } else {
        drawCow(cowX, cowY, velocity);
      }

      // Hiển thị điểm số & giao diện
      if (gameState === "PLAYING") {
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#1e3799";
        ctx.lineWidth = 4;
        ctx.font = "bold 44px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.strokeText(score, cvs.width / 2, 70);
        ctx.fillText(score, cvs.width / 2, 70);
      } else if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 26px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
        ctx.shadowBlur = 6
