$(document).ready(function () {
    var gameInterval; // Variable to store the interval ID
    var snakeImg = new Image();
    var foodImages = {
        apple: '/static/images/apple.webp',
        banana: '/static/images/banana.webp',
        cherry: '/static/images/cherry.webp'
    };

    // Preload snake image
    snakeImg.src = '/static/images/snakehead2.png';

    // Preload food images
    var foodImgs = {};
    for (var fruit in foodImages) {
        var img = new Image();
        img.src = foodImages[fruit];
        foodImgs[fruit] = img;
    }

    // Function to initialize the game
    function initializeGame() {
        // Clear the existing interval if it exists
        clearInterval(gameInterval);

        // Initialize the game
        $.get('/start', function (data) {
            console.log(data.message);
        });

        var lastDirection = 'RIGHT';
        var gameIsOver = false;

        // Function to update the game state on the canvas
        function updateGame() {
            $.get('/state', function (data) {
                var canvas = document.getElementById('gameCanvas');
                var ctx = canvas.getContext('2d');
                var food = data.food;
                var snake = data.snake;
                var cellSize = 20; // The size of a single cell in the game, 1 food = cell 
                var foodX = food[0] * cellSize;
                var foodY = food[1] * cellSize;

                // Clear the canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Draw the snake
                for (var i = 0; i < snake.length; i++) {
                    var cell = snake[i];
                    var snakeX = cell[0] * cellSize;
                    var snakeY = cell[1] * cellSize;
                    ctx.drawImage(snakeImg, snakeX, snakeY, cellSize, cellSize);
                }

                // Draw the food using the preloaded image based on the selected fruit
                var selectedFruit = $('#fruitSelect').val();
                ctx.drawImage(foodImgs[selectedFruit], foodX, foodY, cellSize, cellSize);

                $('#score').text('Score: ' + data.score);
            });
        }

        function GameOver() {
            // Clear the existing interval if it exists
            clearInterval(gameInterval);

            window.location.href = "/game_over";
        }
        // Function to handle user input and send it to the server
        function handleInput(direction) {

            $.ajax({
                url: '/move',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ direction: direction }),
                success: function (data) {
                    console.log(data.message);
                    updateGame();

                    if (data.gameOver) {
                        gameIsOver = true;
                        GameOver();
                    }
                }
            });
        }

        $(document).keydown(function (e) {
            switch (e.which) {
                case 37: // left arrow
                    lastDirection = 'LEFT';
                    break;

                case 38: // up arrow
                    lastDirection = 'UP';
                    break;

                case 39: // right arrow
                    lastDirection = 'RIGHT';
                    break;

                case 40: // down arrow
                    lastDirection = 'DOWN';
                    break;

                default:
                    return;
            }
            e.preventDefault();
        });

        // Set the interval and store the interval ID in the gameInterval variable
        gameInterval = setInterval(function () {
            // Get the last known direction and continue moving
            handleInput(lastDirection);
        }, 80); // Speed of the snake, lower is faster

        updateGame();
    }
    // Call the initializeGame function when the start button is clicked
    $('#startButton').on('click', function () {
        // Load the first food image based on the selected fruit
        initializeGame();
    });

    // Call the initializeGame function when the enter key is pressed
    document.addEventListener('keydown', function(event) {
        if (event.keyCode === 13) {
            
            initializeGame();
        }
    });
    // Call the initializeGame function when the dropdown value changes
    $('#fruitSelect').on('change', function () {
        // Load the first food image based on the selected fruit
        initializeGame();
    });

});
