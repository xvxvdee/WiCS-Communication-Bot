# WiCS-Communication-Bot

This is a Discord bot that posts internship and new-grad roles

## Features

- Scrapes job postings from [SimplifyJobs](https://github.com/SimplifyJobs) Summer 2024 Internships and New Grad repos 
- Posts jobs to a specified Discord channel every day
- Provides a link to apply for each job

## Installation

- Clone this repository: `git clone https://github.com/xvxvdee/WiCS-Communication-Bot.git`
- Install the required packages: `pip install -r requirements.txt`
- Create a Discord bot account and get a token: https://discord.com/developers/docs/intro
- Create a MongoDB account and get a connection string: https://www.mongodb.com/cloud/atlas
- Create a .env file in the root directory and add the following variables:

```
DISCORD_TOKEN=<your discord bot token>
MONGO_URI=<your mongodb connection string>
```

- Run the bot: `python DiscordBot.py`
