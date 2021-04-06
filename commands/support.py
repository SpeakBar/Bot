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
    bot.add_cog(Support(bot))

with open(path + '/json/dashboard.json') as data:
    dashboard = json.load(data)

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(reaction, user):
        if reaction.message.author == bot.user:
            return

        for support in int(dashboard['ticket_channel']):
            if reaction.message.channel == support:
                if reaction.emoji == "✉️":
                    print('ok')
    
    @commands.command()
    async def ticket(self, ctx):
        embed = discord.Embed(title="Ticket support", description="Ticket de support, clicker sur la réaction '✉️' pour en ouvrir 1.", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✉️')