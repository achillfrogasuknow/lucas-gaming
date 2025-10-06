const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");

const paddleHeight = 80;
const paddleWidth = 12;
const ballRadius = 10;

let playerY = canvas.height / 2 - paddleHeight / 2;
let computerY = canvas.height / 2 - paddleHeight / 2;
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;
let ballSpeedX = 5;
let ballSpeedY = 3;

let playerDir = 0; // -1 up, 1 down, 0 none
let playerSpeed = 6;
let playerScore = 0;
let computerScore = 0;
let gameOver = false;

document.addEventListener("keydown", handleKey);

function handleKey(e) {
  const key = e.key.toLowerCase();
  if (key === "w") playerDir = -1;
  else if (key === "s") playerDir = 1;
}

function drawRect(x, y, w, h, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

function drawCircle(x, y, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2, false);
  ctx.closePath();
  ctx.fill();
}

function resetBall() {
  ballX = canvas.width / 2;
  ballY = canvas.height / 2;
  ballSpeedX = -ballSpeedX;
  ballSpeedY = 3 * (Math.random() > 0.5 ? 1 : -1);
}

function update() {
  if (gameOver) return;

  // Move player paddle continuously
  playerY += playerDir * playerSpeed;
  if (playerY < 0) playerY = 0;
  if (playerY > canvas.height - paddleHeight) playerY = canvas.height - paddleHeight;

  // Computer AI
  let compCenter = computerY + paddleHeight / 2;
  if (compCenter < ballY - 30) computerY += 5;
  else if (compCenter > ballY + 30) computerY -= 5;

  // Move ball
  ballX += ballSpeedX;
  ballY += ballSpeedY;

  // Bounce top/bottom
  if (ballY + ballRadius > canvas.height || ballY - ballRadius < 0)
    ballSpeedY = -ballSpeedY;

  // Player paddle collision
  if (
    ballX - ballRadius < paddleWidth &&
    ballY > playerY &&
    ballY < playerY + paddleHeight
  ) {
    ballSpeedX = -ballSpeedX;
    let deltaY = ballY - (playerY + paddleHeight / 2);
    ballSpeedY = deltaY * 0.25;
  }

  // Computer paddle collision
  if (
    ballX + ballRadius > canvas.width - paddleWidth &&
    ballY > computerY &&
    ballY < computerY + paddleHeight
  ) {
    ballSpeedX = -ballSpeedX;
    let deltaY = ballY - (computerY + paddleHeight / 2);
    ballSpeedY = deltaY * 0.25;
  }

  // Left/right edge → score
  if (ballX - ballRadius < 0) {
    computerScore++;
    document.getElementById("score").innerText =
      playerScore + " - " + computerScore;
    resetBall();
  } else if (ballX + ballRadius > canvas.width) {
    playerScore++;
    document.getElementById("score").innerText =
      playerScore + " - " + computerScore;
    resetBall();
  }

  // End condition
  if (playerScore === 5 || computerScore === 5) {
    document.getElementById("status").innerText =
      playerScore > computerScore ? "🏆 You Win!" : "💀 You Lose!";
    gameOver = true;
  }
}

function draw() {
  drawRect(0, 0, canvas.width, canvas.height, "rgba(0, 0, 0, 0.7)");

  // Middle dashed line
  for (let i = 0; i < canvas.height; i += 20) {
    drawRect(canvas.width / 2 - 1, i, 2, 10, "#00ffcc");
  }

  // Paddles
  drawRect(0, playerY, paddleWidth, paddleHeight, "#00f7ff");
  drawRect(canvas.width - paddleWidth, computerY, paddleWidth, paddleHeight, "#ff007f");

  // Ball
  drawCircle(ballX, ballY, ballRadius, "#ffffff");

  update();
}

function gameLoop() {
  draw();
  if (!gameOver) requestAnimationFrame(gameLoop);
}

function startGame() {
  playerScore = 0;
  computerScore = 0;
  document.getElementById("score").innerText = "0 - 0";
  document.getElementById("status").innerText = "";
  gameOver = false;
  resetBall();
  gameLoop();
}

startGame();