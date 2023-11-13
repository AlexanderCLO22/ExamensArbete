$(document).ready(function () {
    var gameInterval; // Variable to store the interval ID
    var snakeImg = new Image();
    var foodImages = [
        '/static/images/apple.webp',
        '/static/images/banana.webp',
        '/static/images/cherry.webp'
    ];

    // Preload snake image
    snakeImg.src = '/static/images/snakehead2.png';

    // Preload food images
    var foodImgs = [];
    for (var i = 0; i < foodImages.length; i++) {
        var img = new Image();
        img.src = foodImages[i];
        foodImgs.push(img);
    }

    var currentFoodImageIndex = 0; // Index to keep track of the current food image

    // Function to load the next food image
    function loadNextFoodImage() {
        currentFoodImageIndex = (currentFoodImageIndex + 1) % foodImgs.length;
        initializeGame(); // Start the game after loading the next food image
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

                // Draw the food using the preloaded image
                ctx.drawImage(foodImgs[currentFoodImageIndex], foodX, foodY, cellSize, cellSize);

                $('#score').text('Score: ' + data.score);
            });
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

    // Call the loadNextFoodImage function when a button with the id 'startButton' is clicked
    $('#startButton').on('click', function () {
        // Load the first food image
        loadNextFoodImage();
    });
});