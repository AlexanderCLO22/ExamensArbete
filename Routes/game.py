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
    snake_game = snake.SnakeGame()
    # Skapar en ny game state i databasen
    current_app.mongodb_repository.create_or_replace_game_state(current_user.id, snake_game.grid_size, snake_game.snake, snake_game.food, snake_game.direction, snake_game.last_direction, snake_game.score, snake_game.gameOver)
    return jsonify({'message': 'Game started'})

@gameviews.route('/state')
def get_state():
    game_state = current_app.mongodb_repository.get_game_state(current_user.id)
    return jsonify({
        'snake': game_state['snake'],
        'food': game_state['food'],
        'direction': game_state['direction'],
        'score': game_state['score']
    })

@gameviews.route('/move', methods=['POST'])
def move():
    game_state = current_app.mongodb_repository.get_game_state(current_user.id)
    game_state['last_direction'] = game_state['direction']
    data = request.json
    direction = data.get('direction')
    
    if direction == 'UP' and game_state['last_direction'] == 'DOWN':
        direction = 'DOWN'
    elif direction == 'DOWN' and game_state['last_direction'] == 'UP':
        direction = 'UP'
    elif direction == 'LEFT' and game_state['last_direction'] == 'RIGHT':
        direction = 'RIGHT'
    elif direction == 'RIGHT' and game_state['last_direction'] == 'LEFT':
        direction = 'LEFT'

    # Update the game state based on user input
    game_state['direction'] = direction
    game_state['gameOver'] = False  # Reset game over flag

    # Use the SnakeGame class to update the game state
    snake_game = snake.SnakeGame()
    snake_game.update_game_state(game_state)

    # Store the updated game state in the database
    current_app.mongodb_repository.create_or_replace_game_state(
        current_user.id,
        game_state['grid_size'],
        game_state['snake'],
        game_state['food'],
        game_state['direction'],
        game_state['last_direction'],
        game_state['score'],
        game_state['gameOver']
    )

    if game_state['gameOver']:
        return jsonify({'message': 'Game Over', 'score': game_state['score'], 'gameOver': True})

    return jsonify({'message': 'Moved successfully'})

@gameviews.route('/game_over', methods=['GET'])
def game_over():
    if current_user.is_anonymous:
        return redirect(url_for('homeviews.home'))
    game_state = current_app.mongodb_repository.get_game_state(current_user.id)
    global_highscores = current_app.mongodb_repository.get_all_highscores()
    personal_highscores = current_app.mongodb_repository.get_personal_highscores(current_user.id)
    return render_template('game_over.html', global_highscores=global_highscores, personal_highscores=personal_highscores, score=game_state['score'])


@gameviews.route('submit_score', methods=['GET'])
def submit_score():
    game_state = current_app.mongodb_repository.get_game_state(current_user.id)
    score = game_state['score']
    user = current_user.id
    current_app.mongodb_repository.create_highscore(user, score)
    return redirect(url_for('gameviews.game'))