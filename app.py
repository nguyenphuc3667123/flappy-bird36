import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flying Cow Game", layout="centered")

st.title("🐄 Flappy Flying Cow")
st.write("Dùng phím **Space** hoặc **Click chuột** vào khung game để giúp chú bò bay lên!")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    canvas {
      border: 3px solid #333;
      background-color: #70c5ce;
      display: block;
      margin: 0 auto;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <canvas id="canvas" width="320" height="480"></canvas>
  <script>
    const cvs = document.getElementById("canvas");
    const ctx = cvs.getContext("2d");

    let cowX = 50;
    let cowY = 150;
    let gravity = 0.25;
    let velocity = 0;
    let jump = -4.5;
    let score = 0;

    let pipes = [];
    pipes[0] = { x: cvs.width, topHeight: 150, gap: 120 };

    document.addEventListener("keydown", function(e) {
      if (e.code === "Space") velocity = jump;
    });
    cvs.addEventListener("click", function() {
      velocity = jump;
    });

    function drawCow(x, y) {
      ctx.save();
      ctx.translate(x, y);
      
      // Thân bò (màu trắng đốm đen)
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.ellipse(0, 0, 18, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#333";
      ctx.stroke();

      // Đốm đen trên thân bò
      ctx.fillStyle = "#333333";
      ctx.beginPath();
      ctx.arc(-5, -3, 5, 0, Math.PI * 2);
      ctx.fill();

      // Đầu bò
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(14, -4, 9, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Mõm bò (hồng)
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(19, -2, 4, 3, 0, 0, Math.PI * 2);
      ctx.fill();

      // Sừng bò
      ctx.fillStyle = "#d3d3d3";
      ctx.beginPath();
      ctx.moveTo(12, -12);
      ctx.lineTo(15, -17);
      ctx.lineTo(17, -12);
      ctx.fill();
      ctx.stroke();

      // Cánh vẫy (đặc trưng bò biết bay)
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.ellipse(-2, -14, 8, 4, -Math.PI / 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function draw() {
      ctx.fillStyle = "#70c5ce";
      ctx.fillRect(0, 0, cvs.width, cvs.height);

      // Cập nhật vị trí bò
      velocity += gravity;
      cowY += velocity;

      // Vẽ chú bò
      drawCow(cowX, cowY);

      for (let i = 0; i < pipes.length; i++) {
        ctx.fillStyle = "#2e8b57";
        ctx.fillRect(pipes[i].x, 0, 45, pipes[i].topHeight);
        ctx.fillRect(pipes[i].x, pipes[i].topHeight + pipes[i].gap, 45, cvs.height);

        pipes[i].x -= 2;

        if (pipes[i].x === 120) {
          pipes.push({
            x: cvs.width,
            topHeight: Math.floor(Math.random() * 180) + 50,
            gap: 120
          });
        }

        // Kiểm tra va chạm (tính theo kích thước thân bò)
        if (
          cowX + 15 > pipes[i].x && cowX - 15 < pipes[i].x + 45 &&
          (cowY - 12 < pipes[i].topHeight || cowY + 12 > pipes[i].topHeight + pipes[i].gap) ||
          cowY + 12 > cvs.height || cowY - 12 < 0
        ) {
          location.reload(); // Thua thì làm lại từ đầu
        }

        if (pipes[i].x === 50) score++;
      }

      // Hiển thị điểm số
      ctx.fillStyle = "#fff";
      ctx.font = "bold 22px Arial";
      ctx.fillText("Score: " + score, 15, 35);

      requestAnimationFrame(draw);
    }

    draw();
  </script>
</body>
</html>
"""

components.html(game_code, height=520)
