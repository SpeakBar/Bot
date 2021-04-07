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
    
    @commands.command(help="permet de faire une blague.")
    async def joke(self, ctx):
        headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzgwODE0OTUxMjI4MjQ0MDE4IiwibGltaXQiOjEwMCwia2V5IjoiUEl4QTBjc1pFUExPTEtEYk1KOG9PQ2Y1ZGl6aEdvMWhYZkY5QU5hR0FLM2JzUHU3U3MiLCJjcmVhdGVkX2F0IjoiMjAyMS0wMS0yNlQxNjo1Mzo0OCswMDowMCIsImlhdCI6MTYxMTY4MDAyOH0.dDquxoNTr8sfS1pR0XPetNPxIQ2IwfT7Cwejf4CZq9g'}
        r = requests.get('https://www.blagues-api.fr/api/random', headers=headers)
        data = r.json()

        await ctx.send(data['joke'])
        await asyncio.sleep(1)
        await ctx.send(data['answer'])