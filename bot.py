# Imported Modules
import discord
import os
import re
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


# On connection to discord.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# When a message is sensed in the server.
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    else:
        print(f"{msg.channel}: {msg.author.id}: {msg.author.name}: {msg.content}")
        # general help tutorial. Make sure to update this properly.
        if msg.content.startswith('I love you'):
            await msg.channel.send('I\'m not ready for this level of commitment. :flushed:')
        if msg.content.startswith('$how?'):
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
                birthday_month = date[0]
                birthday_date = date[1]
                if check_month(birthday_month):
                    date_works = check_date(birthday_month, birthday_date)
                    if date_works:
                        birthday = {"_id": msg.author.id, "user": msg.author.name, "month": birthday_month,
                                    "day": birthday_date}
                        await msg.channel.send(f'Adding your birthday, {msg.author.name}!')
                        collection.insert_one(birthday)
                        await msg.channel.send(f'I\'ll send you a birthday wish on {birthday_month}-{birthday_date}!')
                    else:
                        await msg.channel.send('Please enter a DATE within the MONTH that you chose.')
                else:
                    await msg.channel.send('Please enter a number corresponding to a month from 1 to 12.')
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
                await msg.channel.send(f'{msg.author.name}\'s birthday has been removed from the database.')
                collection.find_one_and_delete({"_id": msg.author.id})


client.run(os.environ.get("TOKEN"))


def check_date(month, day):
    if int(month) in [12, 10, 8, 7, 5, 3, 1]:
        if int(day) in range(1, 31):
            return True
        else:
            return False
    elif int(month) in [4, 6, 9, 11]:
        if int(day) in range(1, 30):
            return True
        else:
            return False
    elif int(month) == 2:
        if int(day) in range(1, 28):
            return True
        else:
            return False


def check_month(month):
    return int(month) in range(1, 12)
