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
    bot.add_cog(CommandesAnim(bot))

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

    @commands.command(help="Donne une réponse alléatoire a votre question.")
    async def ask(self, ctx):
        reponse = ["Oui.", "Non.", "Peut-être.", "Certainement pas.", "Carrément.", "Oui.... Mais non.", "Absolument"]
        await ctx.send(random.choice(reponse))

    @commands.command(help="permet de faire une blague.")
    async def joke(self, ctx):
        headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzgwODE0OTUxMjI4MjQ0MDE4IiwibGltaXQiOjEwMCwia2V5IjoiUEl4QTBjc1pFUExPTEtEYk1KOG9PQ2Y1ZGl6aEdvMWhYZkY5QU5hR0FLM2JzUHU3U3MiLCJjcmVhdGVkX2F0IjoiMjAyMS0wMS0yNlQxNjo1Mzo0OCswMDowMCIsImlhdCI6MTYxMTY4MDAyOH0.dDquxoNTr8sfS1pR0XPetNPxIQ2IwfT7Cwejf4CZq9g'}
        r = requests.get('https://www.blagues-api.fr/api/random', headers=headers)
        data = r.json()

        await ctx.send(data['joke'])
        await asyncio.sleep(1)
        await ctx.send(data['answer'])

class CommandesAnim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Hug quelqu'un ou vous même.")
    async def hug(self, ctx, user : discord.User):
        """ Hug! """

        if ctx.message.mentions:
            embed = discord.Embed(description = f"{ctx.message.author.name} fait un câlin {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+hug'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)	
    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description = f"{ctx.message.author.name} fait un câlin personne.", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+hug'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)
	
    @commands.command()
    async def cry(self, ctx, user : discord.User):
        """ Cry! """

        if ctx.message.mentions:
            embed = discord.Embed(description = f"{ctx.message.author.name} pleure sur l'épaule de {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+cry'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)
    @cry.error
    async def cry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(description = f"{ctx.message.author.name} pleure", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+cry'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)

    @commands.command()
    async def kiss(self, ctx, user : discord.User):
        """ Kiss! """

        if ctx.message.mentions:
            embed = discord.Embed(description = f"{ctx.message.author.name} fait la biz à {user.name}", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+kiss'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)
    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(description = f"{ctx.message.author.name} fait la biz à personne...", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_image(url = gif_api('anim+kiss'))
            embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed = embed)
