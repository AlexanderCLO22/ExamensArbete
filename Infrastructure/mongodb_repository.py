from pymongo import MongoClient
from Application.User.user_model import User

class MongoDBRepository:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://AleOje:sIS81pn7svhDCnUm@examensarbete.jv5yrm5.mongodb.net/')
        self.db = self.client['ExamensArbete']
        self.collection_users = self.db['Users']
        self.collection_highscores = self.db['Highscores']
    
    def create_user(self, username, password, email):
        user = User(username=username, password=password, email=email)
        self.collection_users.insert_one(user.__dict__)

    
