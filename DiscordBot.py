import discord #import discord library
import os #used for the token variable, requires that we use .env file
import requests
import base64
import json
from JobScrapingService import JobScrapingService #used to import the job scraping class from the job scrape py
# create a .env file with the token name; find a way to make a private doc on github since the bot will not be run locally

posting = JobScrapingService
client = discord.Client() #connection to discord

@client.event #register event: ready for use
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event #register event: recieve message and execute
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'): #needs to be some sort of trigger; not sure what it should be or how to enable it
        await message.channel.send(posting) #posting needs to be formattd; not sure how to do that...

client.run(os.getenv('TOKEN')) #runs the bot with the login token from the .env file
