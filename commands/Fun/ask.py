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
from class_folder.fun_class import Fun_Class
gifs = Fun_Class()

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(Fun(bot))

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Donne une réponse alléatoire a votre question.")
    async def ask(self, ctx):
        reponse = ["Oui.", "Non.", "Peut-être.", "Certainement pas.", "Carrément.", "Oui.... Mais non.", "Absolument"]
        await ctx.send(random.choice(reponse))