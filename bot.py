# Imports at the top of the file
from my_imports import *
import bot_functions


# On connection to discord.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# When a message is sensed in the server.
@client.event
async def on_message(message):
    # Prevents the bot from reading its own messages
    if message.author == client.user:
        return
    else:
        print(f"{message.channel}: {message.author.id}: {message.author.name}: {message.content}")
        if message.content.startswith('I love you'):
            await message.channel.send('I\'m not ready for this level of commitment. :flushed:')
        # If the user asks for help.
        if message.content.startswith('$how?'):
            await bot_functions.bot_help(message)
        if message.content.startswith('$check_bdays'):
            await bot_functions.check_birthdays(message)
        if message.content.startswith('$add_my_bday:'):
            await bot_functions.add_birthday(message)
        if message.content.startswith('$remove_my_bday'):
            await bot_functions.remove_birthday(message)
        if message.content.startswith('$update_birthday:'):
            await bot_functions.update_birthday(message)


client.run(os.environ.get("TOKEN"))
