<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flappy Flying Cow</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #1e272c;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
      overflow: hidden;
      font-family: Arial, sans-serif;
      touch-action: manipulation;
    }
    h1 {
      color: #fff;
      margin-bottom: 8px;
      font-size: 1.5rem;
    }
    canvas {
      border: 3px solid #fff;
      background: #70c5ce;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      border-radius: 8px;
      outline: none;
    }
  </style>
</head>
<body>

  <h1>🐄 Flappy Flying Cow</h1>
  <canvas id="gameCanvas" width="320" height="480" tabindex="1"></canvas>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let cowX = 60, cowY = 200;
    let gravity = 0.18, lift = -4.2, velocity = 0;
    let score = 0, bestScore = 0;
    let isGameOver = false, gameStarted = false;
    let groundX = 0, frameCount = 0;

    let pipes = [];
    pipes[0] = { x: canvas.width, topHeight: 130, gap: 130, passed: false };

    function resetGame() {
      if (score > bestScore) bestScore = score;
      cowY = 200;
      velocity = 0;
      score = 0;
      pipes = [{ x: canvas.width, topHeight: 130, gap: 130, passed: false }];
      isGameOver = false;
      gameStarted = true;
    }

    function triggerAction(e) {
      if (e) e.preventDefault();
      if (!gameStarted) {
        gameStarted = true;
      } else if (isGameOver) {
        resetGame();
      } else {
        velocity = lift;
      }
    }

    window.addEventListener("keydown", (e) => {
      if (e.code === "Space") triggerAction(e);
    });
    canvas.addEventListener("click", triggerAction);
    canvas.addEventListener("touchstart", triggerAction, { passive: false });
    canvas.focus();

    function drawCow(x, y, vel) {
      ctx.save();
      ctx.translate(x, y);
      let rot = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, vel * 0.08));
      ctx.rotate(rot);

      // Wings
      let wingAngle = Math.sin(frameCount * 0.4) * 0.5;
      ctx.save();
      ctx.translate(-2, -8);
      ctx.rotate(wingAngle);
      ctx.fillStyle = "#fff";
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(0, -4, 7, 3.5, -Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Body
      ctx.fillStyle = "#fff";
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(0, 0, 16, 11, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Spots
      ctx.fillStyle = "#333";
      ctx.beginPath();
      ctx.arc(-3, -2, 4.5, 0, Math.PI * 2);
      ctx.arc(3, 3, 2.5, 0, Math.PI * 2);
      ctx.fill();

      // Head
      ctx.fillStyle = "#fff";
      ctx.beginPath();
      ctx.arc(12, -4, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Snout
      ctx.fillStyle = "#ffb6c1";
      ctx.beginPath();
      ctx.ellipse(17, -2, 3.5, 2.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Eye
      ctx.fillStyle = "#000";
      ctx.beginPath();
      ctx.arc(14, -6, 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Horns
      ctx.fillStyle = "#dcdde1";
      ctx.beginPath();
      ctx.moveTo(9, -10);
      ctx.lineTo(12, -15);
      ctx.lineTo(15, -10);
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function update() {
      frameCount++;

      // Background
      ctx.fillStyle = "#70c5ce";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Clouds
      ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
      ctx.beginPath();
      ctx.arc(50, 80, 20, 0, Math.PI * 2);
      ctx.arc(70, 70, 15, 0, Math.PI * 2);
      ctx.arc(240, 140, 25, 0, Math.PI * 2);
      ctx.fill();

      if (gameStarted && !isGameOver) {
        velocity += gravity;
        cowY += velocity;

        groundX -= 2;
        if (groundX <= -24) groundX = 0;

        // Pipes
        for (let i = 0; i < pipes.length; i++) {
          ctx.fillStyle = "#73bf2e";
          ctx.strokeStyle = "#558022";
          ctx.lineWidth = 2;

          let pWidth = 50;
          let p = pipes[i];

          // Top Pipe
          ctx.fillRect(p.x, 0, pWidth, p.topHeight);
          ctx.strokeRect(p.x, 0, pWidth, p.topHeight);
          ctx.fillRect(p.x - 3, p.topHeight - 18, pWidth + 6, 18);
          ctx.strokeRect(p.x - 3, p.topHeight - 18, pWidth + 6, 18);

          // Bottom Pipe
          let botY = p.topHeight + p.gap;
          ctx.fillRect(p.x, botY, pWidth, canvas.height - 70 - botY);
          ctx.strokeRect(p.x, botY, pWidth, canvas.height - 70 - botY);
          ctx.fillRect(p.x - 3, botY, pWidth + 6, 18);
          ctx.strokeRect(p.x - 3, botY, pWidth + 6, 18);

          p.x -= 2;

          if (p.x === 130) {
            pipes.push({
              x: canvas.width,
              topHeight: Math.floor(Math.random() * 140) + 40,
              gap: 130,
              passed: false
            });
          }

          if (p.x < -60) pipes.shift();

          if (!p.passed && p.x + pWidth < cowX) {
            score++;
            p.passed = true;
          }

          // Collision Check
          let radius = 13;
          if (
            cowX + radius > p.x && cowX - radius < p.x + pWidth &&
            (cowY - radius < p.topHeight || cowY + radius > botY) ||
            cowY + radius >= canvas.height - 70 || cowY - radius <= 0
          ) {
            isGameOver = true;
          }
        }
      }

      // Ground
      ctx.fillStyle = "#ded895";
      ctx.fillRect(0, canvas.height - 70, canvas.width, 70);
      ctx.fillStyle = "#558022";
      ctx.fillRect(0, canvas.height - 70, canvas.width, 14);

      ctx.fillStyle = "#d0342c";
      for (let g = groundX; g < canvas.width; g += 24) {
        ctx.beginPath();
        ctx.moveTo(g, canvas.height - 70);
        ctx.lineTo(g + 12, canvas.height - 70);
        ctx.lineTo(g + 4, canvas.height - 56);
        ctx.lineTo(g - 8, canvas.height - 56);
        ctx.fill();
      }

      // Cow draw
      if (!gameStarted) {
        let hoverY = 200 + Math.sin(frameCount * 0.1) * 6;
        drawCow(cowX, hoverY, 0);
      } else {
        drawCow(cowX, cowY, velocity);
      }

      // UI Screens
      if (!gameStarted) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fff";
        ctx.font = "bold 20px Arial";
        ctx.textAlign = "center";
        ctx.fillText("Click or Press Space to Start", canvas.width / 2, canvas.height / 2);
      } else if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Score board
        ctx.fillStyle = "#ded895";
        ctx.strokeStyle = "#558022";
        ctx.lineWidth = 2;
        ctx.fillRect(60, 120, 200, 160);
        ctx.strokeRect(60, 120, 200, 160);

        ctx.fillStyle = "#b59e54";
        ctx.font = "bold 20px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, 150);

        ctx.fillStyle = "#558022";
        ctx.font = "15px Arial";
        ctx.textAlign = "left";
        ctx.fillText("SCORE", 85, 190);
        ctx.fillText("BEST", 85, 230);

        ctx.textAlign = "right";
        ctx.fillStyle = "#fff";
        ctx.font = "bold 18px Arial";
        ctx.fillText(score, 235, 190);
        ctx.fillText(bestScore, 235, 230);

        ctx.textAlign = "center";
        ctx.fillStyle = "#fff";
        ctx.font = "bold 15px Arial";
        ctx.fillText("Click to Restart", canvas.width / 2, 310);
      } else {
        ctx.fillStyle = "#fff";
        ctx.strokeStyle = "#000";
        ctx.lineWidth = 3;
        ctx.font = "bold 32px Arial";
        ctx.textAlign = "center";
        ctx.strokeText(score, canvas.width / 2, 50);
        ctx.fillText(score, canvas.width / 2, 50);
      }

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
