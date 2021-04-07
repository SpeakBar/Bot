import discord
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from discord.utils import get

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
    async def on_member_join(self, member):
        with open(path + '/json/channel.json', encoding="utf8") as data:
            channel = json.load(data)
        
        server = member.guild
        channel_server = server.text_channels
        
        WelcomeReplica = random.choice(channel['welcome']['sentences'])
        WelcomeReplica = WelcomeReplica.replace('{user}', f'{member.mention}')
        WelcomeReplica = WelcomeReplica.replace('{server}', f'{member.guild}')
        
        for wc in channel['welcome']['channel']:
            if get(channel_server, id=int(wc)):
                await self.bot.get_channel(int(wc)).send(WelcomeReplica)
        