import random

class SnakeGame:
    def __init__(self):
        self.grid_size = 1
        self.snake = 1
        self.food = 1
        self.direction = "" 

    def generate_food(self):
        return random.randint(1, self.grid_size), random.randint(1, self.grid_size)

    def move_snake(self, direction):
        head_x, head_y = self.snake[0]
        if direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
            
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def start_game(self, grid_size):
        self.snake = [(random.randint(1, grid_size), random.randint(1, grid_size))]
        self.food = self.generate_food()
        self.direction = 'RIGHT'