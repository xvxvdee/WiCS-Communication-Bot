import discord #import discord library
import os #used for the token variable, requires that we use .env file
import requests
import base64
import json
from discord.ext import commands
from JobScrapingService import JobScrapingService #used to import the job scraping class from the job scrape py
# create a .env file with the token name; find a way to make a private doc on github since the bot will not be run locally

posting = JobScrapingService

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.command(name='jobs') #command for job posting, preceded with ! 
async def jobPostings(ctx):
        embed = discord.Embed(
            title = "", #main title of the bot or posting type (job apps, incoming internships, etc)
                #url = "" will make this optional, but we can attach a URL to the title if we want
                description = "Looking for your next job? Take a look a these new postings!", #subheading for the posting
                color = discord.Color.blue())
        embed.set_field(name="****", value="", url="", inline=False) 
            #add the posting name in bold letters, value will be the company name, url will be the link to apply
            #we can add as many of these as we want; working on finding a way to do this for as many posting as we need; will try to make a loop if possible
    embed.set_footer(text="") #add text to the footer; maybe a link to a job site or some other job finding resource   
    await ctx.send(embed=embed)

bot.run(TOKEN) #runs the bot with the login token from the .env file; need to find a way to link it..
