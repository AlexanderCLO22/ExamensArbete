const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const segmentSize = 20;  // Adjust the segment size based on your game

let snake = [];
let food = {};
let direction = '';

document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowUp' && direction !== 'DOWN') {
        direction = 'UP';
    } else if (event.key === 'ArrowDown' && direction !== 'UP') {
        direction = 'DOWN';
    } else if (event.key === 'ArrowLeft' && direction !== 'RIGHT') {
        direction = 'LEFT';
    } else if (event.key === 'ArrowRight' && direction !== 'LEFT') {
        direction = 'RIGHT';
    }
});

function initializeGame() {
    snake = [{ x: 2, y: 2 }];  // Initial position of the snake
    food = generateFood();
    direction = 'RIGHT';
}

function generateFood() {
    return {
        x: Math.floor(Math.random() * (canvas.width / segmentSize)),
        y: Math.floor(Math.random() * (canvas.height / segmentSize))
    };
}

function updateCanvas() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the snake
    ctx.fillStyle = 'green';
    snake.forEach(segment => {
        ctx.fillRect(segment.x * segmentSize, segment.y * segmentSize, segmentSize, segmentSize);
    });

    // Draw the food
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x * segmentSize, food.y * segmentSize, segmentSize, segmentSize);
}

function moveSnake() {
    const head = Object.assign({}, snake[0]);  // Create a copy of the head
    switch (direction) {
        case 'UP':
            head.y -= 1;
            break;
        case 'DOWN':
            head.y += 1;
            break;
        case 'LEFT':
            head.x -= 1;
            break;
        case 'RIGHT':
            head.x += 1;
            break;
    }

    // Check for collisions with the food
    if (head.x === food.x && head.y === food.y) {
        snake.unshift(food);  // Add the food to the front of the snake
        food = generateFood();  // Generate new food
    } else {
        snake.pop();  // Remove the last segment of the snake
        snake.unshift(head);  // Add the new head to the front
    }
}
const moveInterval = 70;  // Adjust the speed of the game
let lastMoveTime = 0;
let gameRunning = true;


function gameLoop(currentTime) {
    if (!gameRunning) {
        return;
    }

    const deltaTime = currentTime - lastMoveTime;

    if (deltaTime > moveInterval) {
    moveSnake();
    updateCanvas();
    lastMoveTime = currentTime;
}
requestAnimationFrame(gameLoop);

}

// Start the game
initializeGame();
gameLoop();

// Add an event listener to start a new game
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        initializeGame();
    }
});

