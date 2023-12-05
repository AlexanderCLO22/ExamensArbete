import random

class SnakeGame:
    def __init__(self):
        self.grid_size = 25
        self.snake = [(0, 0)]
        self.food = self.generate_food()
        self.direction = 'RIGHT'
        self.last_direction = self.direction
        self.score = 0
        self.gameOver = False

    def generate_food(self):
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food

    def move(self):
        head = self.snake[0]
        if self.direction == 'UP':
            new_head = (head[0], (head[1] - 1))
        elif self.direction == 'DOWN':
            new_head = (head[0], (head[1] + 1))
        elif self.direction == 'LEFT':
            new_head = ((head[0] - 1), head[1])
        elif self.direction == 'RIGHT':
            new_head = ((head[0] + 1), head[1])

    
        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            self.gameOver = True
            return
     
        self.snake.insert(0, new_head)
      
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            
        else:
            self.snake.pop()
 