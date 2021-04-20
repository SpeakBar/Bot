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

# class
from class_folder.feeling_class import Feeling_Class
gifs = Feeling_Class()

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(test(bot))

class test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help2(self, ctx):
        print(self.bot.cogs)