import discord #import discord library
import os #used for the token variable, requires that we use .env file
# create a .env file with the token name (can also input it directly into the program)
  # https://www.geeksforgeeks.org/how-to-get-discord-token/

client = discord.Client() #connection to discord

@client.event #register event
async def on_ready(): #ready for use message
    print('We have logged in as {0.user}'.format(client))

@client.event #register event
async def on_message(message): #recieves message and acts accordingly 
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('TOKEN')) #runs the bot with the login token from the .env file
