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
    bot.add_cog(Feeling(bot))

class Feeling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="")
    async def eat(self, ctx, user : discord.User):
        """ Eat! """

        if ctx.message.mentions:
            embed = discord.Embed(description = f"{ctx.message.author.name} mange avec {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gifs.gif_api('anim+eat'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)	
    @eat.error
    async def eat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description = f"{ctx.message.author.name} mange seul.", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gifs.gif_api('anim+eat'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)