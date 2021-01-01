# Imported Modules
import discord
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# connecting to the MongoDB server, then the database, then the collection.
cluster = MongoClient(f'{os.environ.get("CONNECTION_URL")}')
db = cluster["user_data"]
collection = db["user_birthdays"]

# Initializing instances of the used objects. Also calling the function to load from .env files.
client = discord.Client()
today = datetime.today()
