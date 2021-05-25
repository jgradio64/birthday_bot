# birthday_bot
A birthday recording and wishing bot for discord!

---

## About this bot
This bot was build using:
* Python
* Discord.py
* MongoDB
* Pymongo


* Upcoming updates will include:
  * Automated checking for birthdays!
  * Snarky replies to random phrases!
  * ~~Updating your birthdate without deleting the old data.~~

---

## Functionality of "birthday_bot"
1. Add a discord user's birthday to a database when prompted.
2. Remove a user's birthday from a database when prompted.
3. Check for server users' birthdays when prompted.
4. Provide instructions on how to use the bot to a user, when prompted.

---

## Getting Started
Make sure you have **administrator privileges** for the server where you want to use the birthday_bot. 
[Check here](https://support.discord.com/hc/en-us/articles/206029707-How-do-I-set-up-Permissions-) if you are having 
problems. You may have to ask a server's administrators to add the bot.

Add the birthday_bot to your Discord server by clicking this 
[link](https://discord.com/api/oauth2/authorize?client_id=793931013050335293&permissions=519232&scope=bot),
then choose which server where you want the bot to be added.

---

## Getting help in the Discord channel
For a quick-help guide type "$how?" into the channel chat and press enter.

---

## Adding your birthday.
Into the discord channel which the bot is added to, enter "$add_my_bday:" followed by 
the numerical value of the month, a dash, and then date.

Example: ```$add_my_bday: 2-29```

Birthdays are added for the user that entered them, you cannot add other users' birthdays.

---

## Removing your birthday.
If you want to remove your birthday from the server, simply enter "$remove_my_bday" into the channel chat.

Example: ```$remove_my_bday```

This will remove the birthday of the user entering the message.

---

## Checking for birthdays.
If you want to check what birthdays are happening on the current day, type "$check_bdays" into the channel and press enter.

Example: ```$check_bdays```

This will check the birthday's of all the members in the server who have recorded their birthdays.

---

## Updating your birthday
Into the discord channel which the bot is added to, enter "$update_birthday:" followed by 
the numerical value of the month, a dash, and then date.

Example: `$update_birthday: 11-17`

This will update the user's birthday to the date given.
