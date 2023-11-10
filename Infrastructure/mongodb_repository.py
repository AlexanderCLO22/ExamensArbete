from pymongo import MongoClient
from Application.User.user_model import User

class MongoDBRepository:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://AleOje:sIS81pn7svhDCnUm@examensarbete.jv5yrm5.mongodb.net/')
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

