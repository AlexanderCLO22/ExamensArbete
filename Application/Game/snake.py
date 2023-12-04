import random

class SnakeGame:
    def __init__(self):
        # Initialize the game state
        self.grid_size = 25
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

    def update_game_state(self, game_state):
        # Move the snake based on the current direction
        head = game_state['snake'][0]
        if game_state['direction'] == 'UP':
            new_head = (head[0], (head[1] - 1))
        elif game_state['direction'] == 'DOWN':
            new_head = (head[0], (head[1] + 1))
        elif game_state['direction'] == 'LEFT':
            new_head = ((head[0] - 1), head[1])
        elif game_state['direction'] == 'RIGHT':
            new_head = ((head[0] + 1), head[1])

        # Check for collisions with the snake itself and the walls

        
        if new_head in game_state['snake'][1:] or new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            game_state['gameOver'] = True
            return

        # Update the snake position
        game_state['snake'].insert(0, new_head)

        # Check for collisions with food
        food_x, food_y = game_state['food']
        if new_head[0] == food_x and new_head[1] == food_y:
            game_state['score'] += 1
            game_state['food'] = self.generate_food()
        else:
            # Remove the last segment of the snake if no food is eaten
            game_state['snake'].pop()
 