import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Flying Cow - Infinite Endless",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        h1 { color: #1e3799; text-align: center; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 2.2rem; margin-bottom: 0px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
        .instructions { text-align: center; color: #485460; font-size: 1rem; margin-bottom: 15px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐄 Flappy Flying Cow (Bản Chuẩn Vô Hạn)</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn phím <b>Space</b> hoặc <b>Click chuột</b> để điều khiển chú bò bay lượn liên tục qua các ống nước!</div>", unsafe_allow_html=True)

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
      box-shadow: 0 12px 30px rgba(0,0,0,0.25);
      border-radius: 12px;
      outline: none;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="340" height="490" tabindex="1"></canvas>
  <script>
    const cvs = document.getElementById("gameCanvas");
    const ctx = cvs.getContext("2d");

    let cowX = 70, cowY = 210;
    let gravity = 0.14, velocity = 0, jump = -3.6;
    let score = 0, bestScore = 0;
    let gameState = "START"; // START, PLAYING, GAMEOVER
    let groundX = 0;
    let frameCount = 0;

    let clouds = [
      { x: 50, y: 90, speed: 0.3, size: 25 },
      { x: 210, y: 150, speed: 0.3, size: 20 },
      { x: 300, y: 70, speed: 0.3, size: 30 }
    ];

    let pipes = [];

    function initGame() {
      cowY = 210;
      velocity = 0;
      score = 0;
      pipes = [{ x: cvs.width, topHeight: 140, gap: 135, passed: false }];
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
        if (c.x < -60) c.x = cvs.width + 60;
      }

      if (gameState === "PLAYING") {
        velocity += gravity;
        cowY += velocity;

        groundX -= 1.8;
        if (groundX <= -28) groundX = 0;

        // Xử lý ống liên tục và kiểm tra va chạm
        for (let i = 0; i < pipes.length; i++) {
          let pWidth = 54;
          let pipeGrad = ctx.createLinearGradient(pipes[i].x, 0, pipes[i].x + pWidth, 0);
          pipeGrad.addColorStop(0, "#2ecc71");
          pipeGrad.addColorStop(0.5
