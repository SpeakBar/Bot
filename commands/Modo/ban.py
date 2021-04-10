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
from discord_webhook import DiscordWebhook, DiscordEmbed

from discord import Webhook, AsyncWebhookAdapter
import aiohttp

import json

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(Moderation(bot))

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user, *reason):
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason = reason)
                await ctx.send(f"{user} à été unban.")
                return
        #Ici on sait que lutilisateur na pas ete trouvé
        await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def bansId(self, ctx):
        ids = []
        bans = await ctx.guild.bans()
        for i in bans:
            ids.append(str(i.user.id))
        await ctx.send("La liste des id des utilisateurs bannis du serveur est :")
        await ctx.send("\n".join(ids))