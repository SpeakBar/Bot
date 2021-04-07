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

def gif_api(search):
    apikey = "LIVDSRZULELA"  # test value
    lmt = 20

    # our test search
    search_term = search
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    d = r.json()

    g = []

    for t in d['results']:
        for gt in t['media']:
            g.append(gt['gif']['url'])
    
    return random.choice(g)

def setup(bot):
    bot.add_cog(Fun(bot))

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Permet de voir votre avatar ou l'avatar d'un autre user.")
    async def avatar(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"Voici l'avatar de {user.name} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    @avatar.error
    async def avatar_error(self, ctx, error):
        embed = discord.Embed(title=f"Voici l'avatar de {ctx.message.author.name} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.set_image(url=ctx.message.author.avatar_url)
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command(help="Pong!")
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong ! 🏓 `{int(ping)}ms`")