import discord 
import time
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
    
    try:
        send_new_grad_roles.start()
    except Exception as ex:
        print(f"EXCEPTION TASK START:\n>New grad roles\n>{ex}")
    try:
        send_summer_roles.start()
    except Exception as ex:
        print(f"EXCEPTION TASK START:\n>Summer roles\n>{ex}")
    try:
        send_offseason_roles.start()
    except Exception as ex:
        print(f"EXCEPTION TASK START:\n>Offseason roles\n>{ex}")



@tasks.loop(hours=24)
async def send_new_grad_roles():
    job_channel = client.get_channel(1202309603602464768)
    plugs = client.get_channel(817211947908595713)
    df_posting = job_fetcher.latest_newgrad_postings()
    newgrad_color = 0xf2f0ff

    try:
        for i, row in df_posting.iterrows():
            print(f"Posting New Grad role ... {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)}")
            if data_accessor.get_posted(row): 
                print(f"> {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)} was already posted today.\n")
                continue
            else:
                embed=discord.Embed(description="New Grad", title=data_accessor.get_company_text(row), color=newgrad_color)
                embed.set_thumbnail(url=newgrad_icon)
                embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
                embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
                embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
                embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
                embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
                
                try:
                    await job_channel.send(embed=embed)
                    await plugs.send(embed=embed)
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/newgrad_postings.csv",header=True, index=True)
                except Exception as e:
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/newgrad_postings.csv",header=True, index=True)
                    print(f"New grad role {data_accessor.get_company_text(row)} failed to send.\n{str(e)}")
                time.sleep(5);

    except(AttributeError) as err:
        print(f"TASK ERROR: While sending New Grad roles...\n{err}")
        return


@tasks.loop(hours=24)
async def send_summer_roles():
    job_channel = client.get_channel(1202309603602464768)
    df_posting = job_fetcher.latest_internship_postings()
    summer_color = 0xd1c171
    try:
        for i, row in df_posting.iterrows():
            print(f"Posting internship ... {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)}")
            if data_accessor.get_posted(row): 
                print(f"> {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)} was already posted today.\n")
                continue
            else:
                embed=discord.Embed(description="Summer Internship", title=data_accessor.get_company_text(row), color=summer_color)
                embed.set_thumbnail(url=internship_icon)
                embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
                embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
                embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
                embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
                embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
                try:
                    await job_channel.send(embed=embed)
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/internship_postings.csv",header=True, index=True)

                except Exception as e:
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/newgrad_postings.csv",header=True, index=True)
                    print(f"Internship role {data_accessor.get_company_text(row)} failed to send.\n{str(e)}")
                time.sleep(5);
    except(AttributeError) as err:
        print(f"TASK ERROR: While sending Internship roles...\n{err}")
        return

@tasks.loop(hours=24)
async def send_offseason_roles():
    job_channel = client.get_channel(1202309603602464768)
    df_posting = job_fetcher.latest_offseason_postings()
    offseason_color = 0x71b4d1

    try:
        for i, row in df_posting.iterrows():
            print(f"Posting offseason internship ... {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)}")
            if data_accessor.get_posted(row): 
                print(f"> {data_accessor.get_company_text(row)}: {data_accessor.get_role(row)} was already posted today.\n")
                continue
            else:
                embed=discord.Embed(description="Offseason Internship", title=data_accessor.get_company_text(row), color=offseason_color)
                embed.set_thumbnail(url=offseason_icon)
                embed.add_field(name="Role", value=data_accessor.get_role(row), inline=True)
                embed.add_field(name="Date Posted", value=data_accessor.get_date_posted(row), inline=True)
                embed.add_field(name="Term(s)", value=data_accessor.get_terms(row), inline=False)
                embed.add_field(name="Location", value=data_accessor.get_locations(row), inline=False)
                embed.add_field(name="Application Link", value=data_accessor.get_application_link(row), inline=False)
                embed.set_footer(text="Resume icons created by juicy_fish - Flaticon")
                
                try:
                    await job_channel.send(embed=embed)
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/offseason_postings.csv",header=True, index=True)

                except Exception as e:
                    data_accessor.update_posted_status(i,df_posting)
                    df_posting.to_csv("Data/newgrad_postings.csv",header=True, index=True)
                    print(f"Offseason role {data_accessor.get_company_text(row)} failed to send.\n{str(e)}")
                time.sleep(5)

    except(AttributeError) as err:
        print(f"TASK ERROR: While sending Offseason internship roles...\n{err}")
        return

client.run(TOKEN) #runs the bot with the login token from the .env file


