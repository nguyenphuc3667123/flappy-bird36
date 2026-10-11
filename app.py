import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Flying Cow - Infinite Mode",
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

st.markdown("<h1>🐄 Flappy Flying Cow (Chế độ Vô Hạn)</h1>", unsafe_allow_html=True)
st.markdown("<div class='instructions'>Nhấn phím <b>Space</b> hoặc <b>Click chuột</b> để điều khiển chú bò bay lượn vô tận không sợ chết!</div>", unsafe_allow_html=True)

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
    let score = 0;
    let groundX = 0;
    let frameCount = 0;

    let clouds = [
      { x: 50, y: 90, speed: 0.3, size: 25 },
      { x: 210, y: 150, speed: 0.3, size: 20 },
      { x: 300, y: 70, speed: 0.3, size: 30 }
    ];

    let pipes = [{ x: cvs.width, topHeight: 140, gap: 135, passed: false }];

    function handleInput(e) {
      if (e.code === "Space" || e.type === "click") {
        velocity = jump;
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

      // Vật lý chú bò
      velocity += gravity;
      cowY += velocity;

      // Giới hạn trần và sàn để bò không bị bay ra ngoài màn hình
      if (cowY < 15) { cowY = 15; velocity = 0; }
      if (cowY > cvs.height - 95) { cowY = cvs.height - 95; velocity = 0; }

      groundX -= 1.8;
      if (groundX <= -28) groundX = 0;

      // Xử lý ống chạy vô hạn (Không có va chạm chết)
      for (let i = 0; i < pipes.length; i++) {
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
        ctx.fillRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);
        ctx.strokeRect(pipes[i].x - 4, pipes[i].topHeight - 22, pWidth + 8, 22);

        // Ống dưới
        let botY = pipes[i].topHeight + pipes[i].gap;
        ctx.fillRect(pipes[i].x, botY, pWidth, cvs.height - 85 - botY);
        ctx.strokeRect(pipes[i].x, botY, pWidth, cvs.height - 85 - botY);
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

        // Tăng điểm khi vượt qua ống
        if (!pipes[i].passed && pipes[i].x + pWidth < cowX) {
          score++;
          pipes[i].passed = true;
        }
      }

      // Vẽ mặt đất
      let groundY = cvs.height - 85;
      ctx.fillStyle = "#f1c40f";
      ctx.fillRect(0, groundY, cvs.width, 85);
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

      // Vẽ chú bò
      drawCow(cowX, cowY, velocity);

      // Hiển thị điểm số vô tận
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = "#1e3799";
      ctx.lineWidth = 4;
      ctx.font = "bold 38px 'Segoe UI', sans-serif";
      ctx.textAlign = "center";
      ctx.strokeText(score, cvs.width / 2, 60);
      ctx.fillText(score, cvs.width / 2, 60);

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
"""

components.html(game_code, height=520)
