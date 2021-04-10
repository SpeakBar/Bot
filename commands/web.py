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
    bot.add_cog(Web(bot))

class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def jobs(self, ctx):
        job = requests.post("https://speakbar.fr/api/jobs", data={'valide': 'yes'})
    
    @commands.command(aliases=['user_info'])
    async def ui(self, ctx, user : discord.User):
        user_id = user.id

        ui = requests.post("https://speakbar.fr/api/user", data={'discord_id': user_id})
        data_ui = ui.json()

        print(data_ui)

        # Send
        try:
            # Embed
            embed = discord.Embed(title=f"Information SpeakBar sur {user.name} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.set_author(name=f"{data_ui['user']['pseudo']}", icon_url=f"{data_ui['user']['avatar']}", url=f"https://speakbar.fr")
            embed.set_thumbnail(url=f" {data_ui['user']['avatar']} ")

            embed.add_field(name="Pseudo :", value=f"``` {data_ui['user']['pseudo']} ```", inline=True)
            embed.add_field(name="Crée le :", value=f"``` {data_ui['user']['created_at']} ```", inline=True)
            embed.add_field(name="Biographie :", value=f"``` {data_ui['user']['bio']} ```", inline=False)

            embed.set_footer(text=f" {ctx.message.author.name} ", icon_url=f" {ctx.message.author.avatar_url} ")

            await ctx.send(embed=embed)
        except Exception as exception:
            # Embed
            embed = discord.Embed(title=f"Information SpeakBar sur {user.name} ", description=f"Se compte n\'existe pas.", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))

            await ctx.send(embed=embed)
    @ui.error
    async def ui_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            user_id = ctx.message.author.id

            ui = requests.post("https://speakbar.fr/api/user", data={'discord_id': user_id})
            data_ui = ui.json()

            # Send
            try:
                # Embed
                embed = discord.Embed(title=f"Information SpeakBar sur {ctx.message.author.name} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
                embed.set_author(name=f"{data_ui['user']['pseudo']}", icon_url=f"{data_ui['user']['avatar']}", url=f"https://speakbar.fr")
                embed.set_thumbnail(url=f" {data_ui['user']['avatar']} ")

                embed.add_field(name="Pseudo :", value=f"``` {data_ui['user']['pseudo']} ```", inline=True)
                embed.add_field(name="Crée le :", value=f"``` {data_ui['user']['created_at']} ```", inline=True)
                embed.add_field(name="Biographie :", value=f"``` {data_ui['user']['bio']} ```", inline=False)

                embed.set_footer(text=f" {ctx.message.author.name} ", icon_url=f" {ctx.message.author.avatar_url} ")

                await ctx.send(embed=embed)
                
            except:
                # Embed
                embed = discord.Embed(title=f"Information SpeakBar sur {ctx.message.author.name} ", description=f"Se compte n\'existe pas.", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))

                await ctx.send(embed=embed)
            
            return
        
        print(f"Erreur : {error}")
    
    @commands.command(help="Commande pour m'inviter sur votre serveur.", aliases=["me"])
    async def invite(self, ctx):
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=782173199710289992&permissions=8&scope=bot')