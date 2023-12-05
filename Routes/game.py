from flask import Blueprint, current_app, jsonify, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from Application.Game import snake

gameviews = Blueprint('gameviews', __name__)

@login_required
@gameviews.route('/game')
def game():
    if current_user.is_anonymous:
        return redirect(url_for('homeviews.home'))
    
    global_highscores = current_app.mongodb_repository.get_all_highscores()
    personal_highscores = current_app.mongodb_repository.get_personal_highscores(current_user.id)
    return render_template('game.html', global_highscores=global_highscores, personal_highscores=personal_highscores)

@gameviews.route('/start')
def start_game():
    global snake_game
    snake_game = snake.SnakeGame()
    return jsonify({'message': 'Game started'})

@gameviews.route('/state')
def get_state():
    return jsonify({
        'snake': snake_game.snake,
        'food': snake_game.food,
        'direction': snake_game.direction,
        'score': snake_game.score
    })

@gameviews.route('/move', methods=['POST'])
def move():
    snake_game.last_direction = snake_game.direction
    data = request.json
    direction = data.get('direction')
    
    if direction == 'UP' and snake_game.last_direction == 'DOWN':
        direction = 'DOWN'
    elif direction == 'DOWN' and snake_game.last_direction == 'UP':
        direction = 'UP'
    elif direction == 'LEFT' and snake_game.last_direction == 'RIGHT':
        direction = 'RIGHT'
    elif direction == 'RIGHT' and snake_game.last_direction == 'LEFT':
        direction = 'LEFT'

    snake_game.direction = direction
    snake_game.move()

    if snake_game.gameOver:
        return jsonify({'message': 'Game Over', 'score': snake_game.score, 'gameOver': True})

    return jsonify({'message': 'Moved successfully'})

@gameviews.route('/game_over', methods=['GET'])
def game_over():
    if current_user.is_anonymous:
        return redirect(url_for('homeviews.home'))

    global_highscores = current_app.mongodb_repository.get_all_highscores()
    personal_highscores = current_app.mongodb_repository.get_personal_highscores(current_user.id)
    return render_template('game_over.html', global_highscores=global_highscores, personal_highscores=personal_highscores, score=snake_game.score)


@gameviews.route('submit_score', methods=['GET'])
def submit_score():
    score = snake_game.score
    user = current_user.id
    current_app.mongodb_repository.create_highscore(user, score)
    return redirect(url_for('gameviews.game'))