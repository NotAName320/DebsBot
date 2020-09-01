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
    if message.author.id == 750193408781451264 and message.content.startswith('Please vote on'):
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await message.add_reaction('🟡')
        await message.add_reaction('🔐')
    if message.content.startswith('db!'):
        command = message.content.replace("db!", "")
        params = command.split()
        if command.startswith('bill'):
            try:
                response = requests.get(params[1])
                embedDesc = "Yea ✅ - 0 votes\n\nNay ❌ - 0 votes\n\nAbstain 🟡 - 0 votes"
                time.sleep(1)  # To give Discord time to process the embed. Reduces the chance of a "No titles found"
                # error preventing the message from going through.
                billEmbed = discord.Embed(title="Vote on Bill", description=embedDesc, color=16711680, url=params[1])
                await message.channel.send('Please vote on "' + message.embeds[0].title + '" <@&717451321636290611>', embed=billEmbed)
            except requests.exceptions.MissingSchema as exception:
                await message.channel.send('Not a valid URL.')
                print(f'Illegal URL logged when attempting to create bill vote.')
        else:
            await message.channel.send('Incorrect command. db!help for a list of available commands.')


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.id == 750193408781451264 and reaction.message.content.startswith('Please vote on') and user.id != 750193408781451264:
        if roleCheck(user.roles, 'Vote Manager') and reaction.emoji == '🔐':
            await reaction.message.edit(content='Vote closed!')
            await reaction.message.channel.send(countVotes(reaction.message.reactions[0].count - 1, reaction.message.reactions[1].count - 1))
        elif roleCheck(user.roles, 'Congress of the Syndicates') and await userCheck(user, reaction.message, reaction.emoji):
            billEmbed = reaction.message.embeds[0]
            billEmbed.description = "Yea ✅ - " + str(reaction.message.reactions[0].count - 1) + " votes\n\nNay ❌ - " + str(reaction.message.reactions[1].count - 1) + " votes\n\nAbstain 🟡 - " + str(reaction.message.reactions[2].count - 1) + " votes"
            await reaction.message.edit(embed=billEmbed)
        else:
            await reaction.remove(user)
            print(f'Illegal vote from ' + user.name + ' detected and removed.')


@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.author.id == 750193408781451264 and reaction.message.content.startswith('Please vote on') and user.id != 750193408781451264:
        billEmbed = reaction.message.embeds[0]
        billEmbed.description = "Yea ✅ - " + str(reaction.message.reactions[0].count - 1) + " votes\n\nNay ❌ - " + str(reaction.message.reactions[1].count - 1) + " votes\n\nAbstain 🟡 - " + str(reaction.message.reactions[2].count - 1) + " votes"
        await reaction.message.edit(embed=billEmbed)


def roleCheck(roles, CheckingName):
    for i in roles:
        if i.name == CheckingName:
            return True


async def userCheck(reactor, message, emoji):
    for reaction in message.reactions:
        if reaction.emoji != emoji:
            async for user in reaction.users():
                if reactor.name == user.name:
                    return False
    return True


def countVotes(Yeas, Nays):
    if Yeas > Nays:
        return 'The Yeas have ' + str(Yeas) + '. The Nays have ' + str(Nays) + '. The Yeas have it.'
    else:
        return 'The Yeas have ' + str(Yeas) + '. The Nays have ' + str(Nays) + '. The Nays have it.'


client.run(TOKEN)
