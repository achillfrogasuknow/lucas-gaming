const canvas = document.getElementById("snakeCanvas");
const ctx = canvas.getContext("2d");
const box = 20;
const canvasSize = 400;

let snake = [{ x: 9 * box, y: 10 * box }];
let direction = "RIGHT";
let food = randomFood();
let score = 0;
let speed = 100; // fast default
let game = null;
let gameOver = false;

document.addEventListener("keydown", handleKey);
document.getElementById("speedBtn").addEventListener("click", toggleSpeed);

function handleKey(e) {
  const key = e.key.toLowerCase();
  if ((key === "a" || e.key === "ArrowLeft") && direction !== "RIGHT") direction = "LEFT";
  else if ((key === "w" || e.key === "ArrowUp") && direction !== "DOWN") direction = "UP";
  else if ((key === "d" || e.key === "ArrowRight") && direction !== "LEFT") direction = "RIGHT";
  else if ((key === "s" || e.key === "ArrowDown") && direction !== "UP") direction = "DOWN";
}

function toggleSpeed() {
  const btn = document.getElementById("speedBtn");
  speed = (speed === 100) ? 200 : 100;
  btn.textContent = speed === 100 ? "Speed: Fast" : "Speed: Slow";
  restartGame(false);
}

function randomFood() {
  return {
    x: Math.floor(Math.random() * (canvasSize / box)) * box,
    y: Math.floor(Math.random() * (canvasSize / box)) * box
  };
}

function collision(head, arr) {
  return arr.some(seg => seg.x === head.x && seg.y === head.y);
}

function draw() {
  if (gameOver) return;

  ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
  ctx.fillRect(0, 0, canvasSize, canvasSize);

  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i === 0 ? "#00ff00" : "#00aa00";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
  }

  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, box, box);

  let headX = snake[0].x;
  let headY = snake[0].y;

  if (direction === "LEFT") headX -= box;
  if (direction === "UP") headY -= box;
  if (direction === "RIGHT") headX += box;
  if (direction === "DOWN") headY += box;

  if (
    headX < 0 || headY < 0 ||
    headX >= canvasSize || headY >= canvasSize ||
    collision({ x: headX, y: headY }, snake)
  ) {
    document.getElementById("status").innerText = "💀 Game Over!";
    clearInterval(game);
    gameOver = true;
    return;
  }

  if (headX === food.x && headY === food.y) {
    score++;
    document.getElementById("score").innerText = score;
    food = randomFood();
  } else {
    snake.pop();
  }

  snake.unshift({ x: headX, y: headY });
}

function restartGame(resetSnake = true) {
  clearInterval(game);
  if (resetSnake) {
    snake = [{ x: 9 * box, y: 10 * box }];
    direction = "RIGHT";
    score = 0;
    gameOver = false;
    document.getElementById("score").innerText = "0";
    document.getElementById("status").innerText = "";
    food = randomFood();
  }
  game = setInterval(draw, speed);
}

// start
restartGame();