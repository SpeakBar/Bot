import discord
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions

import datetime
import time

import asyncio
import random
import requests
import os

import aiohttp

import json

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(Reaction_event(bot))

class Reaction_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        with open(path + '/json/channel.json') as data:
            dashboard = json.load(data)
        with open(path + '/json/bdd.json') as data:
            bdd = json.load(data)

        if reaction.message.author == bot.user:
            return
        
        if reaction.emoji == '🌟':
            if reaction and reaction.count == 1:
                for bs in bdd['stars_message']:
                    if int(bs) == reaction.message.id:
                        return

                server = bot.get_guild(reaction.message.guild.id)
                for c in dashboard['stars_channel']:
                    if server.get_channel(int(c)):

                        channel = server.get_channel(int(c))

                        # Embed
                        embed = discord.Embed(title=f"5 🌟" ,description=reaction.message.content, timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
                        embed.set_footer(icon_url = reaction.message.author.avatar_url, text=reaction.message.author.name)

                        await channel.send(embed=embed)

                ############# BDD ##############
                bdd['stars_message'].append(f'{reaction.message.id}')

                y = json.dumps(bdd)

                f = open(path + "/json/bdd.json", "w")
                f.write(y)
                f.close()
                ############# BDD ##############

                await reaction.message.pin(reason="rien")
                # await reaction.message.add_reaction('🌟')