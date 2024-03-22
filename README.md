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
CHANNEL_ID_1 = <WICS job posting channel id>
SUMMER_LINK = <SimplifyJobs readme link, ex. "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/README.md">
OFFSEASON_LINK = <SimplifyJobs readme link, ex. "https://api.github.com/repos/SimplifyJobs/Summer2024-Internships/contents/README-Off-Season.md?ref=dev">
NEWGRAD_LINK = <SimplifyJobs readme link  ex. "https://api.github.com/repos/SimplifyJobs/New-Grad-Positions/contents/README.md?ref=dev">
```

- Run the bot: `python DiscordBot.py`
