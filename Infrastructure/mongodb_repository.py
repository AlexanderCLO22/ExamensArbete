from pymongo import MongoClient
import pymongo
import os
from Application.User.user_model import User

class MongoDBRepository:
    def __init__(self):
        connstring = os.getenv('MONGODB_CONNECTION_STRING')
        self.client = MongoClient(connstring)
        self.db = self.client['ExamensArbete']
        self.collection_users = self.db['Users']
        self.collection_highscores = self.db['Highscores']
        self.collection_game_states = self.db['Game_State']

    def find_user(self, username):
        user_data = self.collection_users.find_one({"username": username})
        if user_data:
            return User(user_data)
        else:
            return None
        
    def create_user(self, username, password):
        user_data = {'username': username, 'password': password}
        self.collection_users.insert_one(user_data)

    def create_highscore(self, user, score):
        highscore_data = {'user': user, 'score': score}
        self.collection_highscores.insert_one(highscore_data)

    def get_personal_highscores(self, user):
        highscores = self.collection_highscores.find({'user': user}).sort('score', pymongo.DESCENDING)
        return highscores
    
    def get_all_highscores(self):
        highscores = self.collection_highscores.find().sort('score', pymongo.DESCENDING)
        return highscores
    
    def create_or_replace_game_state(self, user_id, grid_size, snake, food, direction, last_direction, score, gameOver):
        # Check if a game state already exists for the user
        game_state = self.get_game_state(user_id)
        if game_state:
            # Update the existing document
            self.update_game_state(user_id, grid_size, snake, food, direction, last_direction, score, gameOver)
        else:
            # Create a new document
            self.collection_game_states.insert_one({
                'user_id': user_id,
                'grid_size': grid_size,
                'snake': snake,
                'food': food,
                'direction': direction,
                'last_direction': last_direction,
                'score': score,
                'gameOver': gameOver
            })

    def get_game_state(self, user_id):
        # Retrieve game state based on user ID
        return self.collection_game_states.find_one({'user_id': user_id})
    
    def update_game_state(self, user_id, grid_size, snake, food, direction, last_direction, score, gameOver):
    # Update the existing document for the specified user_id
        self.collection_game_states.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'grid_size': grid_size,
                    'snake': snake,
                    'food': food,
                    'direction': direction,
                    'last_direction': last_direction,
                    'score': score,
                    'gameOver': gameOver
                }
            }
        )