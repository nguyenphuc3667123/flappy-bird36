import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird Game", layout="centered")

st.title("🐤 Flappy Bird trên Streamlit")
st.write("Nhấn nút **Space** hoặc **Click chuột** vào khung game để nhảy!")

# Đoạn mã HTML/JavaScript tạo game Flappy Bird đơn giản
game_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    canvas {
      border: 2px solid #333;
      background-color: #70c5ce;
      display: block;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <canvas id="canvas" width="320" height="480"></canvas>
  <script>
    const cvs = document.getElementById("canvas");
    const ctx = cvs.getContext("2d");

    let birdX = 50;
    let birdY = 150;
    let gravity = 0.25;
    let velocity = 0;
    let jump = -4.5;
    let score = 0;

    let pipes = [];
    pipes[0] = { x: cvs.width, topHeight: 150, gap: 100 };

    document.addEventListener("keydown", function(e) {
      if (e.code === "Space") velocity = jump;
    });
    cvs.addEventListener("click", function() {
      velocity = jump;
    });

    function draw() {
      // Background
      ctx.fillStyle = "#70c5ce";
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Bird
      velocity += gravity;
      birdY += velocity;
      ctx.fillStyle = "#ff0";
      ctx.beginPath();
      ctx.arc(birdX, birdY, 12, 0, Math.PI * 2);
      ctx.fill();

      // Pipes
      for (let i = 0; i < pipes.length; i++) {
        ctx.fillStyle = "#2e8b57";
        // Ống trên
        ctx.fillRect(pipes[i].x, 0, 40, pipes[i].topHeight);
        // Ống dưới
        ctx.fillRect(pipes[i].x, pipes[i].topHeight + pipes[i].gap, 40, cvs.height);

        pipes[i].x -= 2;

        if (pipes[i].x === 120) {
          pipes.push({
            x: cvs.width,
            topHeight: Math.floor(Math.random() * 200) + 50,
            gap: 100
          });
        }

        // Kiểm tra va chạm
        if (
          birdX + 12 > pipes[i].x && birdX - 12 < pipes[i].x + 40 &&
          (birdY - 12 < pipes[i].topHeight || birdY + 12 > pipes[i].topHeight + pipes[i].gap) ||
          birdY + 12 > cvs.height || birdY - 12 < 0
        ) {
          location.reload(); // Thua thì chơi lại
        }

        if (pipes[i].x === 50) score++;
      }

      // Score
      ctx.fillStyle = "#fff";
      ctx.font = "20px Arial";
      ctx.fillText("Score: " + score, 10, 30);

      requestAnimationFrame(draw);
    }

    draw();
  </script>
</body>
</html>
"""

# Hiển thị game vào Streamlit
components.html(game_code, height=520)
