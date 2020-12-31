# Imported Modules
import discord
import os
import re
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# connecting to the MongoDB server, then the database, then the collection.
cluster = MongoClient(os.getenv("CONNECTION_URL"))
db = cluster["user_data"]
collection = db["user_birthdays"]

# Initializing instances of the used objects. Also calling the function to load from .env files.
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
        # general help tutorial. Make sure to update this properly.
        if msg.content.startswith('I love you'):
            await msg.channel.send('I\'m not ready for this level of commitment. :flushed:')
        if msg.content.startswith('$how??'):
            await msg.channel.send('To check if any one has a birthday today just type "$check_bdays"\n\n\n')
            await msg.channel.send('To add your birthday use "$add_my_bday: Month-Day".\n'
                                   'Use digits for the month and day.\n'
                                   'Example: "$add_my_bday: 11-04"\n\n\n')
            await msg.channel.send('To remove your birthday from the server use "$remove_my_bday"\n\n')

        if msg.content.startswith('$check_bdays'):
            my_query = {"month": f'{today.month}', "day": f'{today.day}'}
            if collection.count_documents(my_query) == 0:
                await msg.channel.send('There are no birthdays today. :weary:')
                print(collection.find(my_query))
            if collection.count_documents(my_query) != 0:
                list_of_birthdays = collection.find(my_query)
                for birthday in list_of_birthdays:
                    await msg.channel.send("Happy birthday " + birthday['user'] + "!!!")
        if msg.content.startswith('$add_my_bday:'):
            my_query = {"_id": msg.author.id}
            # if there is not a preexisting result in the database by that user
            if collection.count_documents(my_query) == 0:
                date = re.findall("([0-9]{2})", msg.content)
                bday_month = date[0]
                bday_date = date[1]
                bday = {"_id": msg.author.id, "user": msg.author.name, "month": bday_month, "day": bday_date}
                await msg.channel.send(f'Adding your birthday, {msg.author.name}!')
                collection.insert_one(bday)
                await msg.channel.send(f'I\'ll send you a birthday wish on {bday_month}-{bday_date}!')
            else:
                # if there is a preexisting result in the database by that user.
                await msg.channel.send("Your birthday is already recorded.")
        if msg.content.startswith('$remove_my_bday'):
            my_query = {"_id": msg.author.id}
            # if there is not a preexisting result in the database by that user
            if collection.count_documents(my_query) == 0:
                await msg.channel.send(f'No birthday was previously recorded for {msg.author.name}.')
            # if there is a preexisting result in the database by that user.
            if collection.count_documents(my_query) > 0:
                await msg.channel.send(f'Working on this feature.')
                collection.find_one_and_delete({"_id": msg.author.id})


client.run(os.getenv("TOKEN"))
