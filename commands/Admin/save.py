import discord
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions

import datetime
import time

import asyncio
import random
import requests

import aiohttp

import json

def setup(bot):
    bot.add_cog(CommandesSave(bot))

class CommandesSave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def save(self, ctx):
        text_channel_list = []
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                text_channel_list.append(channel)
            
        await ctx.send(text_channel_list)