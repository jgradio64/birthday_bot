import discord
import os
import re
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

cluster = MongoClient(os.getenv("CONNECTION_URL"))
db = cluster["user_data"]
collection = db["user_birthdays"]

load_dotenv()
client = discord.Client()
today = datetime.today()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    else:
        print(f"{msg.channel}: {msg.author.id}: {msg.author.name}: {msg.content}")
        if msg.content.startswith('$how??'):
            await msg.channel.send('To check if any one has a birthday today just type "$check_bdays"\n\n\n')
            await msg.channel.send('To add your birthday use "$add_my_bday: Month-Day".\n'
                                   'Use digits for the month and day.\n'
                                   'Example: "$add_my_bday: 11-04"\n\n\n')
            await msg.channel.send('To remove your birthday from the server use "$remove_my_bday"\n\n')

        if msg.content.startswith('$check_bdays'):
            query = {"month": today.month, "day": today.day}
            if collection.count_documents(query) == 0:
                await msg.channel.send('There are no birthdays today. :weary:')
        if msg.content.startswith('$add_my_bday:'):
            myQuery = {"_id": msg.author.id}
            if collection.count_documents(myQuery) == 0:
                date = re.findall("([0-9]{2})", msg.content)
                bday_month = date[0]
                bday_date = date[1]
                bday = {"_id": msg.author.id, "user": msg.author.name, "month": bday_month, "day": bday_date}
                await msg.channel.send(f'Adding your birthday, {msg.author.name}!')
                collection.insert_one(bday)
                await msg.channel.send(f'I\'ll send you a birthday wish on {bday_month}-{bday_date}!')
            else:
                await msg.channel.send("Your birthday is already recorded.")
        if msg.content.startswith('$remove_my_bday'):
            myQuery = {"_id": msg.author.id}
            if collection.count_documents(myQuery) == 0:
                await msg.channel.send(f'No birthday was previously recorded for {msg.author.name}.')
            if collection.count_documents(myQuery) > 0:
                await msg.channel.send(f'Sorry {msg.author.name}, I\'m still working on this feature.')

client.run(os.getenv("TOKEN"))