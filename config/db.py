from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del .env

class MongoDB:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def get_db(self):
        return self.db

db_instance = MongoDB().get_db()