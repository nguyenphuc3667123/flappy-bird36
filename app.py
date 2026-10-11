import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Flying Cow - Deluxe Edition",
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

st.markdown("<h1>🐄 Flappy Flying Cow Deluxe</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn phím <b>Space</b> hoặc <b>Click chuột</b> để điều khiển chú bò bay thong thả lượn sóng!</div>", unsafe_allow_html=True)

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

      // Cánh vẫy hiệu ứng mượt
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

      // Thân bò bóng bẩy
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#1e272c";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 18, 13, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Đốm bò phong cách
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

      // Má hồng dễ thương
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
      // Ánh sáng trong mắt
      ctx.fillStyle = "#fff";
      ctx.beginPath();
      ctx.arc(16.5, -7.5, 0.4, 0, Math.PI * 2);
      ctx.fill();

      // Sừng bóng
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

      // Vẽ nền trời chuyển sắc động
      let bgGrad = ctx.createLinearGradient(0, 0, 0, cvs.height);
      bgGrad.addColorStop(0, "#4a69bd");
      bgGrad.addColorStop(0.5, "#6a89cc");
      bgGrad.addColorStop(1, "#82ccdd");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Vẽ mây trôi
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

        for (let i = 0; i < pipes.length; i++) {
          // Ống nước gradient sinh động
          let pWidth = 54;
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
          // Miệng ống trên
          ctx.fillRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);
          ctx.strokeRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);

          // Ống dưới
          let botY = pipes[i].topHeight + pipes[i].gap;
          ctx.fillRect(pipes[i].x, botY, pWidth, cvs.height - 85 - botY);
          ctx.strokeRect(pipes[i].x, botY, pWidth, cvs.height - 85 - botY);
          // Miệng ống dưới
          ctx.fillRect(pipes[i].x - 4, botY, pWidth + 8, 22);
          ctx.strokeRect(pipes[i].x - 4, botY, pWidth + 8, 22);

          pipes[i].x -= 1.8;

          if (pipes[i].x === 140) {
            pipes.push({
              x: cvs.width,
              topHeight: Math.floor(Math.random() * 170) + 50,
              gap: 135,
              passed: false
            });
          }

          if (pipes[i].x < -70) pipes.shift();

          if (!pipes[i].passed && pipes[i].x + pWidth < cowX) {
            score++;
            pipes[i].passed = true;
          }

          // Va chạm
          if (
            cowX + 15 > pipes[i].x && cowX - 15 < pipes[i].x + pWidth &&
            (cowY - 12 < pipes[i].topHeight || cowY + 12 > botY) ||
            cowY + 13 >= cvs.height - 85 || cowY - 13 <= 0
          ) {
            gameState = "GAMEOVER";
          }
        }
      }

      // Vẽ mặt đất hiện đại, sắc nét
      let groundY = cvs.height - 85;
      ctx.fillStyle = "#f1c40f"; // Đất cát vàng ấm
      ctx.fillRect(0, groundY, cvs.width, 85);
      ctx.fillStyle = "#27ae60"; // Lớp cỏ xanh mướt phía trên
      ctx.fillRect(0, groundY, cvs.width, 18);

      // Đường sọc mặt đất
      ctx.fillStyle = "#d35400";
      for (let g = groundX; g < cvs.width; g += 28) {
        ctx.beginPath();
        ctx.moveTo(g, groundY);
        ctx.lineTo(g + 14, groundY);
        ctx.lineTo(g + 5, groundY + 18);
        ctx.lineTo(g - 9, groundY + 18);
        ctx.fill();
      }

      // Vẽ chú bò
      if (gameState === "START") {
        // Hiệu ứng bồng bềnh nhẹ ở màn hình chờ
        let hoverY = 210 + Math.sin(frameCount * 0.08) * 8;
        drawCow(cowX, hoverY, 0);
      } else {
        drawCow(cowX, cowY, velocity);
      }

      // Giao diện hiển thị điểm & màn hình
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
        ctx.textAlign = "center";
        ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
        ctx.shadowBlur = 6;
        ctx.fillText("Nhấn Space để Bắt Đầu", cvs.width / 2, cvs.height / 2 + 30);
        ctx.shadowBlur = 0;
      } else if (gameState === "GAMEOVER") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        // Bảng điểm hiện đại bo tròn góc
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#1e3799";
        ctx.lineWidth = 3;
        let bx = 50, by = 130, bw = 240, bh = 200, radius = 16;
        
        ctx.beginPath();
        ctx.moveTo(bx + radius, by);
        ctx.lineTo(bx + bw - radius, by);
        ctx.quadraticCurveTo(bx + bw, by, bx + bw, by + radius);
        ctx.lineTo(bx + bw, by + bh - radius);
        ctx.quadraticCurveTo(bx + bw, by + bh, bx + bw - radius, by + bh);
        ctx.lineTo(bx + radius, by + bh);
        ctx.quadraticCurveTo(bx, by + bh, bx, by + bh - radius);
        ctx.lineTo(bx, by + radius);
        ctx.quadraticCurveTo(bx, by, bx + radius, by);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "#e74c3c";
        ctx.font = "bold 24px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", cvs.width / 2, by + 45);

        ctx.fillStyle = "#2f3640";
        ctx.font = "16px 'Segoe UI', sans-serif";
        ctx.textAlign = "left";
        ctx.fillText("Điểm hiện tại", bx + 25, by + 95);
        ctx.fillText("Kỷ lục cao nhất", bx + 25, by + 140);

        ctx.textAlign = "right";
        ctx.font = "bold 20px 'Segoe UI', sans-serif";
        ctx.fillStyle = "#27ae60";
        ctx.fillText(score, bx + bw - 25, by + 95);
        ctx.fillText(bestScore, bx + bw - 25, by + 140);

        // Hướng dẫn chơi lại
        ctx.textAlign = "center";
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 3;
        ctx.font = "bold 16px 'Segoe UI', sans-serif";
        ctx.strokeText("Nhấn Space để chơi lại", cvs.width / 2, 380);
        ctx.fillText("Nhấn Space để chơi lại", cvs.width / 2, 380);
      }

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
"""

components.html(game_code, height=520)
