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

from class_folder.premium_class import Premium_Class
premium = Premium_Class()

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(Premium(bot))

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def premium(self, ctx):

        await premium.check_premium(ctx)

    @commands.command()
    async def p_move(self, ctx, user: discord.User):
        voice_state = ctx.member.voice
        voice_user_state = user.voice