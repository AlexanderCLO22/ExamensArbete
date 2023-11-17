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