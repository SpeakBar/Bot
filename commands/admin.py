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
    bot.add_cog(CommandesAdmin(bot))

class CommandesAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def annonce(self, ctx, args):
        content = "".join(args)

        embed = discord.Embed(title="Annonce", description=f" {content} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.add_field(name="Mention :", value="@everyone")

        await ctx.send(embed=embed)
    
    @commands.command()
    async def move(self, ctx, user):
        author = ctx.message.author
        await client.move_member(author, ctx.author.voice.channel)
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stars_channel(self, ctx):
        with open(path + '/json/channel.json') as data:
            stars = json.load(data)

        if ctx.message.author == self.bot.user:
            return

        for scv in stars['stars']['channel']:
            if ctx.message.channel.id == int(scv):
                msg = await ctx.send('channel déjà enregistrée.')
                await asyncio.sleep(3)
                await ctx.message.delete()
                await msg.delete()
                return

        stars['stars']['channel'].append(f'{ctx.message.channel.id}')

        y = json.dumps(stars)

        f = open(path + "/json/channel.json", "w")
        f.write(y)
        f.close()

        await ctx.send('Channel sauvegarder.')
    
    @commands.command()
    async def annonce_channel(self, ctx):
        with open(path + '/json/channel.json') as data:
            stars = json.load(data)

        stars['annonce']['channel'].append(f'{ctx.message.channel.id}')

        y = json.dumps(stars)

        f = open(path + "/json/channel.json", "w")
        f.write(y)
        f.close()

        await ctx.send('Channel sauvegarder.')
        