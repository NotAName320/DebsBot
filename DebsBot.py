import os

import discord
import requests
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} connected')


@client.event
async def on_message(message):
    if message.content.startswith('db!'):
        command = message.content.replace("db!", "")
        params = command.split()
        if command.startswith('bill'):
            try:
                response = requests.get(params[1])
                embedDesc = "Choice 1 - 0 votes\n\nChoice 2 - 0 votes\n\nChoice 3 - 0 votes"
                time.sleep(1)
                billEmbed = discord.Embed(title="Vote on Bill", description=embedDesc, color=16711680, url=params[1])
                await message.channel.send('Please vote on "' + message.embeds[0].title + '"', embed=billEmbed)
            except requests.exceptions.MissingSchema as exception:
                await message.channel.send('Not a valid URL.')
                print(f'Illegal URL logged when attempting to create bill vote.')
        else:
            await message.channel.send('Incorrect command. db!help for a list of available commands.')


client.run(TOKEN)
