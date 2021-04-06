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
    bot.add_cog(Information(bot))

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['si', 'info', 'server'], help=f" {self.bot.command_prefix}serverInfo ", description="Commande pour connaitre toutes les informations du serveur.")
    async def serverInfo(self, ctx):
        embed = discord.Embed(title=f"Toutes les informations du serveur {ctx.guild.name} ", timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name="Description :", value=f"``` {ctx.guild.description} ```", inline=True)
        embed.add_field(name="Owner :", value=f"``` {ctx.guild.owner} ```", inline=True)
        embed.add_field(name="Region :", value=f"``` {ctx.guild.region} ```", inline=True)

        embed.add_field(name="Date création du serveur :", value=f"``` {ctx.guild.created_at} ```", inline=False)

        embed.add_field(name="Nombre de membres :", value=f"``` {ctx.guild.member_count} ```", inline=True)
        embed.add_field(name="Nombre de salons textuels :", value=f"``` {len(ctx.guild.text_channels)} ```", inline=True)
        embed.add_field(name="Nombre de salons vocaux :", value=f"``` {len(ctx.guild.voice_channels)} ```", inline=True)

        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)
    
    @commands.command(help="Connaitre tout les commande/catégorie.")
    async def help(self,ctx,*cog):
        """Commande."""
        try:
            if not cog:
                halp=discord.Embed(title='Liste des catégorie de commande.',
                                description=f'Utilier `{self.bot.command_prefix}help` pour connaitre tout les categorie de commande ', timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Catégorie',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                await ctx.message.author.send('',embed=halp)
            else:
                if len(cog) > 1:
                    halp = discord.Embed(title='Erreur!',description='C\'est beaucoup trop de Categorie !',color=discord.Color.red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Commandes Listes :',description=self.bot.cogs[cog[0]].__doc__, timestamp = datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        halp = discord.Embed(title='Erreur!',description='Comment utilisez-vous même "'+cog[0]+'"?',color=discord.Color.red())

                    await ctx.message.author.send('',embed=halp)
        except:
            pass

    # @commands.command(aliases=['invite'])
    # async def invites(self, ctx):
    #     totalInvites = 0
    #     for i in await ctx.guild.invites():
    #         if i.inviter == ctx.message.author:
    #             totalInvites += i.uses
    #     await ctx.send(f"Vous avez invité {totalInvites} membre{'' if totalInvites == 1 else 's'} sur se serveur")