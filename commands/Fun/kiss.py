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

    @commands.command()
    async def kiss(self, ctx, user : discord.User):
        """ Kiss! """

        if ctx.message.mentions:
            embed = discord.Embed(description = f"{ctx.message.author.name} fait la biz à {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gifs.gif_api('anim+kiss'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)
    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(description = f"{ctx.message.author.name} fait la biz à personne...", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gifs.gif_api('anim+kiss'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)