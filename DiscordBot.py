import discord 
from discord.ext import tasks,commands
import os
from dotenv import load_dotenv 
from JobPostingFetcher import JobPostingFetcher 
from DataFrameAccessor import DataFrameAccessor

# Setup Bot
load_dotenv()
TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix="$",intents=discord.Intents.default()) 

# Create instances for postings
job_fetcher = JobPostingFetcher()
data_accessor = DataFrameAccessor()
newgrad_icon = "https://cdn-icons-png.flaticon.com/128/1991/1991047.png"
internship_icon = "https://cdn-icons-png.flaticon.com/128/7376/7376577.png"
offseason_icon = "https://cdn-icons-png.flaticon.com/128/2117/2117739.png"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    send_new_grad_roles.start()
    send_summer_roles.start()
    send_offseason_roles.start()

@tasks.loop(hours=24)
async def send_new_grad_roles():
    job_channel = client.get_channel(1202309603602464768)
    plugs = client.get_channel(817211947908595713)

    df_posting = job_fetcher.latest_newgrad_postings()
    newgrad_color = 0xf2f0ff

    try:
        for i, row in df_posting.iterrows():
            embed=discord.Embed(title="NEW GRAD POSTING", description=data_accessor.get_company_text(row), color=newgrad_color)
            embed.set_thumbnail(url=newgrad_icon)
            embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
            embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
            embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
            embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
            embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
            await job_channel.send(embed=embed)
            await plugs.send(embed=embed)
    except(AttributeError) as err:
        print(err)
        return


@tasks.loop(hours=24)
async def send_summer_roles():
    job_channel = client.get_channel(1202309603602464768)
    df_posting = job_fetcher.latest_internship_postings()
    newgrad_color = 0xd1c171
    try:
        for i, row in df_posting.iterrows():
            embed=discord.Embed(title="SUMMER INTERNSHIP POSTING", description=data_accessor.get_company_text(row), color=newgrad_color)
            embed.set_thumbnail(url=internship_icon)
            embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
            embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
            embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
            embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
            embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
            await job_channel.send(embed=embed)
    except(AttributeError) as err:
        print(err)
        return

@tasks.loop(hours=24)
async def send_offseason_roles():
    job_channel = client.get_channel(1202309603602464768)
    df_posting = job_fetcher.latest_offseason_postings()
    newgrad_color = 0x71b4d1

    try:
        for i, row in df_posting.iterrows():
            embed=discord.Embed(title="OFFSEASON INTERNSHIP POSTING", description=data_accessor.get_company_text(row), color=newgrad_color)
            embed.set_thumbnail(url=internship_icon)
            embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
            embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
            embed.add_field(name="Term(s)", value=data_accessor.get_terms(row), inline=False)
            embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
            embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
            embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
            await job_channel.send(embed=embed)
    except(AttributeError) as err:
        print(err)
        return

client.run(TOKEN) #runs the bot with the login token from the .env file


