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
    async def warn(self, ctx, user: discord.User, reason = "Aucune raison donnée."):

        find = True

        embed = discord.Embed(title="Warn", description=f"{user} vient de se faire warn.", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("F6B93B", 16)))
        embed.add_field(name="Modérateur :", value=f" {ctx.message.author.mention} ")
        embed.add_field(name="Utilisateur :", value=f" {user.mention} ")
        embed.add_field(name="Raison :", value=f" {reason} ")
        embed.set_thumbnail(url = user.avatar_url)

        with open(path + '/json/warn.json') as data:
            warn_file = json.load(data)
        
        for w in warn_file['user_warn']:
            if user.id == w['user_id']:

                find = False

                w['nb_warn'] += 1

                with open(path + '/json/warn.json', 'w') as data:
                    json.dump(warn_file, data)

                embed.add_field(name="Nombre de Warn :", value=f" {w['nb_warn']} ")

                if w['nb_warn'] == 3:
                    
                    try:
                        await ctx.guild.kick(user, reason = "3 warn")
                    except:
                        print('ne peux pas être kick')

                elif w['nb_warn'] == 6:
                    try:
                        await ctx.guild.ban(user, reason = "6 warn")
                    except:
                        print('ne peux pas être ban.')

                break

        if find:
            warn_file['user_warn'].append({"user_id": user.id, "nb_warn": 1})

            with open(path + '/json/warn.json', 'w') as data:
                json.dump(warn_file, data)

            embed.add_field(name="Nombre de Warn :", value=f" 1 ")

        await ctx.send(embed=embed)
    
    @commands.command()
    async def warn_remove(self, ctx, user: discord.User, number: int, reason = "Il n'y a pas de raison."):
        no_find = True
        loop = 0

        embed = discord.Embed(title="Remove Warn", description=f"{user} vient de se faire remove_warn.", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("F6B93B", 16)))
        embed.add_field(name="Modérateur :", value=f" {ctx.message.author.mention} ")
        embed.add_field(name="Utilisateur :", value=f" {user.mention} ")
        embed.add_field(name="Raison :", value=f" {reason} ")
        embed.set_thumbnail(url = user.avatar_url)

        with open(path + '/json/warn.json') as data:
            warn_file = json.load(data)
        
        for w in warn_file['user_warn']:

            if user.id == w['user_id']:

                no_find = False

                w['nb_warn'] -= int(number)

                if w['nb_warn'] < 0:
                    w['nb_warn'] = 0
                
                if w['nb_warn'] == 0:
                    del warn_file['user_warn'][loop]

                    with open(path + '/json/warn.json', 'w') as data:
                        json.dump(warn_file, data)

                    break

                with open(path + '/json/warn.json', 'w') as data:
                    json.dump(warn_file, data)

                embed.add_field(name="Nombre de Warn :", value=f" {w['nb_warn']} ")

                break

            loop += 1

        if no_find:
            warn_file['user_warn'].append({"user_id": user.id, "nb_warn": 1})

            with open(path + '/json/warn.json', 'w') as data:
                json.dump(warn_file, data)

            embed.add_field(name="Nombre de Warn :", value=f" 1 ")

        await ctx.send(embed=embed)
    
    @commands.command()
    async def warn_clear(self, ctx, user: discord.User, reason = "Il n'y a aucun raison."):
        no_find = True
        loop = 0

        with open(path + '/json/warn.json') as data:
            warn_file = json.load(data)
        
        for w in warn_file['user_warn']:
            if user.id == w['user_id']:
                no_find = False

                del warn_file['user_warn'][loop]

                with open(path + '/json/warn.json', 'w') as data:
                    json.dump(warn_file, data)

                break
            loop += 1
        
        if no_find:
            reply = await ctx.send("Il n'y a aucun utilisateur à ce nom avec des warn.")
        else:
            reply = await ctx.send(f"Les warn de {user} on bien étaient supprimer.")
        
        await ctx.delete()
        await asyncio.sleep(3)
        await reply.delete()

        