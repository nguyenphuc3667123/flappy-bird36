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
        .main { background: #f0f2f5; }
        h1 { color: #1e3799; text-align: center; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 2.2rem; margin-bottom: 0px; }
        .instructions { text-align: center; color: #57606f; font-size: 1.05rem; margin-bottom: 15px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐄 Flappy Flying Cow</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Press <b>Spacebar</b> or <b>Click</b> inside the game area to fly!</div>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      display: flex;
      justify-content: center;
      background: transparent;
    }
    canvas {
      border: 3px solid #1e3799;
      background: linear-gradient(to bottom, #4a69bd, #786fa6);
      display: block;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
      border-radius: 12px;
      outline: none;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="360" height="540" tabindex="1"></canvas>
  <script>
    const cvs = document.getElementById("gameCanvas");
    const ctx = cvs.getContext("2d");

    let cowX = 80, cowY = 240;
    let gravity = 0.16, velocity = 0, jump = -4.0;
    let score = 0, bestScore = 0;
    let gameState = "START"; // START, PLAYING, GAMEOVER
    let groundX = 0;
    let frameCount = 0;

    let clouds = [
      { x: 50, y: 90, speed: 0.3, size: 26 },
      { x: 220, y: 160, speed: 0.3, size: 20 },
      { x: 320, y: 70, speed: 0.3, size: 30 }
    ];

    let pipes = [];

    function initGame() {
      cowY = 240;
      velocity = 0;
      score = 0;
      pipes = [{ x: cvs.width, topHeight: 160, gap: 140, passed: false }];
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

      // Wing flapping
      let wingAngle = Math.sin(frameCount * 0.35) * 0.55;
      ctx.save();
      ctx.translate(-2, -8);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#2f3640";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.ellipse(0, -5, 8, 4, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Body
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#1e272c";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 17, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Body spots
      ctx.fillStyle = "#1e272c";
      ctx.beginPath();
      ctx.arc(-4, -2, 5, 0, Math.PI * 2);
      ctx.arc(3, 3, 3, 0, Math.PI * 2);
      ctx.fill();

      // Head
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(13, -4, 8.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Pink snout
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(18, -2, 4, 3, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Eye
      ctx.fillStyle = "#000";
      ctx.beginPath();
      ctx.arc(15, -7, 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Horns
      ctx.fillStyle = "#dcdde1";
      ctx.strokeStyle = "#1e272c";
      ctx.lineWidth = 1;
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

      // Sky background
      let bgGrad = ctx.createLinearGradient(0, 0, 0, cvs.height);
      bgGrad.addColorStop(0, "#4a69bd");
      bgGrad.addColorStop(1, "#786fa6");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Clouds
      ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
      for (let c of clouds) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.size, 0, Math.PI * 2);
        ctx.arc(c.x + c.size * 0.6, c.y - c.size * 0.3, c.size * 0.7, 0, Math.PI * 2);
        ctx.arc(c.x + c.size * 1.2, c.y, c.size * 0.8, 0, Math.PI * 2);
        ctx.fill();
        c.x -= c.speed;
        if (c.x < -60) c.x = cvs.width + 60;
      }

      let groundHeight = 85;

      if (gameState === "PLAYING") {
        velocity += gravity;
        cowY += velocity;

        groundX -= 1.8;
        if (groundX <= -28) groundX = 0;

        // Pipe logic
        for (let i = 0; i < pipes.length; i++) {
          let pWidth = 56;
          let pipeGrad = ctx.createLinearGradient(pipes[i].x, 0, pipes[i].x + pWidth, 0);
          pipeGrad.addColorStop(0, "#2ecc71");
          pipeGrad.addColorStop(1, "#1e8449");

          ctx.fillStyle = pipeGrad;
          ctx.strokeStyle = "#145a32";
          ctx.lineWidth = 2;

          // Top pipe
          ctx.fillRect(pipes[i].x, 0, pWidth, pipes[i].topHeight);
          ctx.strokeRect(pipes[i].x, 0, pWidth, pipes[i].topHeight);
          ctx.fillRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);
          ctx.strokeRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);

          // Bottom pipe
          let botY = pipes[i].topHeight + pipes[i].gap;
          ctx.fillRect(pipes[i].x, botY, pWidth, cvs.height - groundHeight - botY);
          ctx.strokeRect(pipes[i].x, botY, pWidth, cvs.height - groundHeight - botY);
          ctx.fillRect(pipes[i].x - 4, botY, pWidth + 8, 22);
          ctx.strokeRect(pipes[i].x - 4, botY, pWidth + 8, 22);

          pipes[i].x -= 1.8;

          if (pipes[i].x === 140) {
            pipes.push({
              x: cvs.width,
              topHeight: Math.floor(Math.random() * 180) + 60,
              gap: 140,
              passed: false
            });
          }

          if (pipes[i].x < -70) pipes.shift();

          if (!pipes[i].passed && pipes[i].x + pWidth < cowX) {
            score++;
            pipes[i].passed = true;
          }

          // Collision check
          let cowRadius = 15;
          if (
            cowX + cowRadius > pipes[i].x && cowX - cowRadius < pipes[i].x + pWidth &&
            (cowY - cowRadius < pipes[i].topHeight || cowY + cowRadius > botY) ||
            cowY + cowRadius >= cvs.height - groundHeight || cowY - cowRadius <= 0
          ) {
            gameState = "GAMEOVER";
          }
        }
      }

      // Ground
      let groundY = cvs.height - groundHeight;
      ctx.fillStyle = "#f1c40f";
      ctx.fillRect(0, groundY, cvs.width, groundHeight);
      ctx.fillStyle = "#27ae60";
      ctx.fillRect(0, groundY, cvs.width, 18);

      ctx.fillStyle = "#d35400";
      for (let g = groundX; g < cvs.width; g += 28) {
        ctx.beginPath();
        ctx.moveTo(g, groundY);
        ctx.lineTo(g + 14, groundY);
        ctx.lineTo(g + 5, groundY + 18);
        ctx.lineTo(g - 9, groundY + 18);
        ctx.fill();
      }

      // Draw cow
      if (gameState === "START") {
        let hoverY = 240 + Math.sin(frameCount * 0.08) * 8;
        drawCow(cowX, hoverY, 0);
      } else {
        drawCow(cowX, cowY, velocity);
      }

      // UI Text & Screens
      if (gameState === "PLAYING") {
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#1e3799";
        ctx.lineWidth = 4;
        ctx.font = "bold 38px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.strokeText(score, cvs.width / 2, 60);
        ctx.fillText(score, cvs.width / 2, 60);
      } else if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 24px 'Segoe UI', sans-serif";
        ctx.textAlign =
