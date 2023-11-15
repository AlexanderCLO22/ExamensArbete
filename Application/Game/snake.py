import random
from flask import current_app
from flask import redirect, render_template, url_for
from flask_login import current_user

class SnakeGame:
    def __init__(self):
        # Initialize the game state
        self.grid_size = 20
        self.snake = [(0, 0)]
        self.food = self.generate_food()
        self.direction = 'RIGHT'
        self.last_direction = self.direction
        self.score = 0
        self.gameOver = False

    def generate_food(self):
        # Generate random food position that is not occupied by the snake
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food

    def move(self):
        # Move the snake based on the current direction
        head = self.snake[0]
        if self.direction == 'UP':
            new_head = (head[0], (head[1] - 1))
        elif self.direction == 'DOWN':
            new_head = (head[0], (head[1] + 1))
        elif self.direction == 'LEFT':
            new_head = ((head[0] - 1), head[1])
        elif self.direction == 'RIGHT':
            new_head = ((head[0] + 1), head[1])

        # Check for collisions with the snake itself
        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            # Handle game over logic (e.g., reset the game)
            # For simplicity, we reset the game here
            
            self.gameOver = True
            return

        # Update the snake position
        self.snake.insert(0, new_head)

        # Check for collisions with food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            
        else:
            # Remove the last segment of the snake if no food is eaten
            self.snake.pop()
 