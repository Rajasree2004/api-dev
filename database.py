from pymongo import MongoClient
import os

MONGO_DETAILS = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

# Create a MongoClient instance
client = MongoClient(MONGO_DETAILS)

# Get the database
database = client['Rajasree-New']

# Get the collection
collection = database['api-dev']