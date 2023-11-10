const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const segmentSize = 20;  // Adjust the segment size based on your game

let snake;
let food;
let direction = '';

document.addEventListener('keydown', function(event) {
    if (event.key.startsWith('Arrow')) {
        const newDirection = event.key.replace('Arrow', '');
        sendMoveRequest(newDirection);
    }
});

function initializeGame(gridSize) {
    fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            gridSize: gridSize
        })
    })
    .then(response => response.json())
    .then(data => {
        snake = data.snake;
        food = data.food;
        direction = 'RIGHT';
        gameLoop();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function startGame() {
    const gridSize = 20;  // Set your desired grid size
    initializeGame(gridSize);
}


function sendMoveRequest(newDirection) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            direction: newDirection
        })
    })
    .then(response => response.json())
    .then(data => {
        snake = data.snake;
        food = data.food;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateCanvas() {
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

function gameLoop() {
    updateCanvas();
    requestAnimationFrame(gameLoop);
}


document.addEventListener('DOMContentLoaded', function() {
    const gridSize = 20;  // Set your desired grid size
    initializeGame(gridSize);
});


// Add an event listener to start a new game
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        initializeGame();
    }
});

