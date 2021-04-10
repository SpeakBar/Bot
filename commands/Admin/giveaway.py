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
    bot.add_cog(Admin(bot))

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def giveaway(self, ctx):

        def check(m):
            return m.author == ctx.message.author

        await ctx.author.send('Donner moi le gain gagnable !')
        gain_msg = await self.bot.wait_for('message', check=check)

        await ctx.author.send("Nombre de gagnants :")
        winner_msg = await self.bot.wait_for('message', check=check)

        await ctx.author.send('Date final (sous se format : `min/heure/jour/mois`) :')
        time_msg = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title="Giveaway ! 🎉", description=f"Un giveaway vient d'être lancé ! vous pouvais gagner un {gain_msg.content} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("F6B93B", 16)))
        embed.add_field(name=f"Gain :", value=f"{gain_msg.content}", inline=False)
        embed.add_field(name=f"Nombre de gagnants :", value=f"{winner_msg.content}", inline=False)
        embed.add_field(name=f"Temps :", value=f"{time_msg.content}", inline=False)
        embed.add_field(name=f"Auteur :", value=f"{ctx.author.mention}", inline=False)

        try:
            verif_number_id = int(winner_msg.content)
        except:
            return ctx.author.send('Le nombre de gagnants doit être un chiffre.')

        ################### Verification du temps ###################

        time_list = time_msg.content.split('/')
        liste = []
        if len(time_list) == 4:
            for tl in time_list:
                try:
                    liste.append(int(tl))
                except:
                    return ctx.author.send("La date final doit être que des chiffre séparer d'un `/`")
            if not liste[0] >= 0 and not liste[0] <= 59:
                return ctx.author.send("Les minutes ne peuvent pas être inférieures à 0 ou supérieur a 59.")
            if not liste[1] >= 0 and not liste[1] < 24:
                return ctx.author.send("Les heures ne peuvent pas être inférieures à 0 ou supérieur a 24.")
            if not liste[2] >= 1 and not liste[2] < 31:
                return ctx.author.send("Les jours ne peuvent pas être inférieures à 1 ou supérieur a 31.")
            if not liste[3] > 1 and not liste[3] < 12:
                return ctx.author.send("Les mois ne peuvent pas être inférieures à 1 ou supérieur a 12.")
        else:
            return ctx.author.send("Hummm, il y a un problème venant de la date d'expiration")

        ################### END Verification du temps ###################

        giveaway_msg = await ctx.send(embed=embed)

        ################### JSON SAVE ################### 
        with open(path + '/json/giveaway.json') as data:
            giveaway_file = json.load(data)
        
        date = datetime.datetime.now()
        date_time = date.strftime("%M/%H/%d/%m")
        
        giveaway_file['giveaway'].append({"server_id": ctx.guild.id, "creator": f"ctx.author", "reward": gain_msg.content, "nb_winner": verif_number_id, "created_at": f"{date_time}", "expire": f"{liste[0]}/{liste[1]}/{liste[2]}/{liste[3]}", "msg_giveaway_id": giveaway_msg.id})

        with open(path + '/json/giveaway.json', 'w') as data:
            json.dump(giveaway_file, data)

        #################  END JSON SAVE #################