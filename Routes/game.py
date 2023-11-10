from flask import Blueprint, jsonify, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from Application.Game import snake

gameviews = Blueprint('gameviews', __name__)
snake_game = snake.SnakeGame()


@gameviews.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("game.html", user=current_user)

@gameviews.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    
    snake_game.start_game(20)
    
    initial_data = {
        'snake': snake_game.snake,
        'food': snake_game.food,
    }
    return jsonify(initial_data)    

@gameviews.route('/move', methods=['GET', 'POST'])
def move():
    global direction
    data = request.get_json()
    direction = data.get('direction', '')
    snake_game.move_snake()

    updated_data = {
        'snake': snake_game.snake,
        'food': snake_game.food
    }
    return jsonify(updated_data)