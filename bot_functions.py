# Imports at the top of the file
from my_imports import *
import re


# Bot help function
async def bot_help(msg):
    await msg.channel.send('To check if any one has a birthday today just type "$check_bdays"\n')
    await msg.channel.send('To add your birthday use "$add_my_bday: Month-Day".\n'
                           'Use digits for the month and day.\n'
                           '\tExample: "$add_my_bday: 11-4"\n')
    await msg.channel.send('To remove your birthday from the server use "$remove_my_bday"\n'
                           '\tExample: "$remove_my_bday"\n')


# Function to check if there are birthdays on the date that this is called.
async def check_birthdays(msg):
    # Set values to check for in the database
    my_query = {"guild_id": msg.guild.id, "month": today.month, "day": today.day}
    # check the number of birthdays recorded in the database
    number_of_birthdays = collection.count_documents(my_query)
    # if there are no birthdays
    if number_of_birthdays == 0:
        await msg.channel.send('There are no birthdays today. :weary:')
    # If birthdays were found
    if number_of_birthdays != 0:
        # Get the birthdays from the database.
        list_of_birthdays = collection.find(my_query)
        if number_of_birthdays == 1:
            await msg.channel.send(f'There is {number_of_birthdays} birthday today!')
        else:
            await msg.channel.send(f'There are {number_of_birthdays} birthdays today!')
        # Loop through the birthdays wishing happy birthday to everyone!
        for birthday in list_of_birthdays:
            await msg.channel.send("Happy birthday " + birthday['user'] + "!!!\t")


# Function to handle adding a user's birthday to the database
async def add_birthday(msg):
    my_query = {"guild_id": msg.guild.id, "_id": msg.author.id}
    # if there is not a preexisting result in the database by that user
    if collection.count_documents(my_query) == 0:
        date = re.findall("([0-9]+)", msg.content)
        # get month value, convert from str to int
        birthday_month = int(date[0])
        # get date value, convert from str to int
        birthday_date = int(date[1])
        # If the month is an acceptable month
        if check_month(birthday_month):
            # If the date is an acceptable value based upon the month
            if check_date(birthday_month, birthday_date):
                # Create Schema for the users birthday
                birthday = create_birthday(msg.author.id, msg.guild.id, msg.author.name, birthday_month, birthday_date)
                await msg.channel.send(f'Adding your birthday, {msg.author.name}!')
                # Insert the data into the Database
                collection.insert_one(birthday)
                await msg.channel.send(f'I\'ll send you a birthday wish on {birthday_month}-{birthday_date}!')
            else:
                # If the date is not an acceptable value based upon the month
                await msg.channel.send('Please enter a DATE within the MONTH that you chose.')
        else:
            # If the month the user entered is not an acceptable month
            await msg.channel.send('Please enter a number corresponding to a month from 1 to 12.')
    else:
        # if there is a preexisting result in the database by that user.
        await msg.channel.send("Your birthday is already recorded.")


# Function to remove a user's birthday
async def remove_birthday(msg):
    my_query = {"guild_id": msg.guild.id, "_id": msg.author.id}
    # if there is not a preexisting result in the database by that user
    if collection.count_documents(my_query) == 0:
        await msg.channel.send(f'No birthday was previously recorded for {msg.author.name}.')
    # if there is a preexisting result in the database by that user.
    if collection.count_documents(my_query) > 0:
        # Find in the database and delete
        collection.find_one_and_delete({"_id": msg.author.id})
        await msg.channel.send(f'{msg.author.name}\'s birthday has been removed from the database.')


# Checks to see if the month is within the range of possible selections
def check_month(month):
    month_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    return month in month_range


# Build a birthday schema based upon input.
def create_birthday(user_id, guild_id, user_name, month, date):
    return {
        "_id": user_id,
        "guild_id": guild_id,
        "user": user_name,
        "month": month,
        "day": date
    }


# Check if the date giving is in the date range, depending on the month.
def check_date(month, day):
    # January, March, May, July, August, October, December
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day in range(1, 31):
            return True
        else:
            return False
    # April, June, September, November
    elif month in [4, 6, 9, 11]:
        if day in range(1, 30):
            return True
        else:
            return False
    # February
    elif month == 2:
        if day in range(1, 28):
            return True
        else:
            return False


async def update_birthday(msg):
    my_query = {"guild_id": msg.guild.id, "_id": msg.author.id}
    # if there is not a preexisting result in the database by that user
    if collection.count_documents(my_query) == 0:
        await msg.channel.send(f'No birthday was previously recorded for {msg.author.name}.')
        # if there is a preexisting result in the database by that user.
    elif collection.count_documents(my_query) > 0:
        date = re.findall("([0-9]+)", msg.content)
        # get month value, convert from str to int
        birthday_month = int(date[0])
        # get date value, convert from str to int
        birthday_date = int(date[1])
        # If the month is an acceptable month
        if check_month(birthday_month):
            # If the date is an acceptable value based upon the month
            if check_date(birthday_month, birthday_date):
                await msg.channel.send(f'Updating your birthday, {msg.author.name}!')
                # Insert the data into the Database
                collection.find_one_and_update(my_query, {"$set": {"month": birthday_month, "day": birthday_date}})
                await msg.channel.send(f'I will now send you a birthday wish on {birthday_month}-{birthday_date}!')
            else:
                # If the date is not an acceptable value based upon the month
                await msg.channel.send('Please enter a DATE within the MONTH that you chose.')
        else:
            # If the month the user entered is not an acceptable month
            await msg.channel.send('Please enter a number corresponding to a month from 1 to 12.')