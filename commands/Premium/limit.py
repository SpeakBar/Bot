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
    async def p_limit(self, ctx, number: int):

        voice_state = ctx.message.author.voice
        channel_id = voice_state.channel.id

        await premium.check_premium(ctx)

        await premium.check_author_voc(ctx, channel_id)

        if number > 99:
            await ctx.send('Vous ne pouvez pas mettre un nombre supérieur à 99.')
            return
        if number < 1:
            await ctx.send('Vous ne pouvez pas mettre un nombre inférieur à 1.')
            return
        if voice_state is None:
            await ctx.send('Vous devez vous trouver dans un salon vocal.')
            return
        await voice_state.channel.edit(user_limit=number)

    @commands.command()
    async def p_limit_remove(self, ctx):
        voice_state = ctx.message.author.voice

        await premium.check_premium(ctx)

        await voice_state.channel.edit(user_limit=None)
        