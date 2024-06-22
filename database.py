from pymongo import MongoClient
from pymongo.database import Database

client: MongoClient = MongoClient()
db: Database = client['checker']

