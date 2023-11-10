from flask import Blueprint, jsonify, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from Application.Game import snake

gameviews = Blueprint('gameviews', __name__)
snake_game = snake.SnakeGame()


@gameviews.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("game.html", user=current_user)

@gameviews.route('/start', methods=['POST'])
@login_required
def start():
    print(request.headers)
    data = request.json
    print(data)
    grid_size = request.get_json().get('gridSize', 1)
    snake_game.start_game(grid_size)
    
    initial_data = {
        'snake': snake_game.snake,
        'food': snake_game.food,
    }
    return jsonify(initial_data)

@gameviews.route('/move', methods=['POST'])
@login_required
def move():
    direction = request.get_json().get('direction', '')
    snake_game.move_snake(direction)
    
    game_data = {
        'snake': snake_game.snake,
        'food': snake_game.food,
    }
    return jsonify(game_data)