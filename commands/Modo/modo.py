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
    bot.add_cog(CommandesKick(bot))

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Mute":
            return role
            
    return await createMutedRole(ctx)

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Mute",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Mute pour mute des gens qui parle trop.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands say
    # @params : self, ctx, args
    # @description : permet d'écire un message avec le bot.
    # @perm : manage_messages
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def say(self, ctx, args):      
        messages = await ctx.channel.history(limit = 1).flatten()
        for message in messages:
            await message.delete()

        await ctx.send("".join(args))

    # Commands clear
    # @params : self, ctx, number
    # @description : permet de suprimet un certain nombre de message.
    # @perm : manage_messages
    @commands.command(aliases=['purge', 'delete_message'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, number : int):
        messages = await ctx.channel.history(limit = number + 1).flatten()
        for message in messages:
            await message.delete()

    # Commands mute
    # @params : self, ctx, member, *reason
    # @description : permet de mute un user.
    # @perm : manage_roles
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member : discord.Member, *reason):
        mutedRole = await getMutedRole(ctx)
        await member.add_roles(mutedRole)

        if reason:
            arg = "".join(reason)
        else:
            arg = "Il n'y a aucun raison."

        embed = discord.Embed(title = "Mute", description = f"{member.mention} a été Mute", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = "Modérateur :", value = ctx.author.name)
        embed.add_field(name = "Raison :", value = arg)

        await ctx.send(embed = embed)

    # Commands unmute
    # @params : self, ctx, member, *reason
    # @description : permet de unmute un user.
    # @perm : manage_roles
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member : discord.Member, *reason):
        mutedRole = await getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason = reason)

        if reason:
            arg = "".join(reason)
        else:
            arg = "Il n'y a aucun raison."
        
        embed = discord.Embed(title = "Mute", description = f"{member.mention} a été UnMute", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = "Modérateur :", value = ctx.author.name)
        embed.add_field(name = "Raison :", value = arg)

        await ctx.send(embed = embed)
    
    @commands.command()
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send('Channel bloquait.')
    
    @commands.command()
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send('Channel débloquait')
    
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        if channel == None: 
            new_channel = await ctx.message.channel.clone(reason="Reload du channel !")
            await nuke_channel.delete()
            await ctx.message.channel.send("Channel bien supprimée puis reconstruit.")
            return

        nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

        if nuke_channel is not None:
            new_channel = await nuke_channel.clone(reason="Reload du channel !")
            await nuke_channel.delete()
            await new_channel.send("Channel bien supprimée puis reconstruit.")

        else:
            await ctx.send(f"Le channel : {channel.name} n'a pas été trouver. ")

class CommandesKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(f"{user} à été kick.")

# class CommandesWarn(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#         global warn_server
#         warn_server=[]
#         global warn_id
#         warn_id=[]
#         global warn_number
#         warn_number=[]

#     @commands.command()
#     @commands.has_permissions(ban_members = True)
#     async def warn(self, ctx,member : discord.User, *raison):
#             global warn_server
#             global warn_id
#             global warn_number
#             server=ctx.message.guild.id
#             warn_ref=int(member.id)
#             user=str(member.name)
#             if server in warn_server:
#                 server_ref=warn_server.index(server)
#                 if warn_ref in warn_id[server_ref]:
#                     warn_id_ref=warn_id[server_ref].index(warn_ref)
#                     warn_number[server_ref].insert(warn_id_ref,warn_number[server_ref][warn_id_ref]+1)

#                     if not raison:
#                         warnRaison = "Aucunne raison donnée."
#                     else:
#                         warnRaison = " ".join(raison)

#                     embed = discord.Embed(title=f"Warn", description=f"Un warn ajouté à {user} ", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
#                     embed.add_field(name="Modérateur :", value=f" {ctx.message.author.name} ")
#                     embed.add_field(name="Joueur :", value=f" {user} ")
#                     embed.add_field(name="Raison :", value=f" {warnRaison} ")
#                     embed.add_field(name="Nombre de Warn :", value=f" {warn_number[server_ref][warn_id_ref]} ")
#                     embed.set_thumbnail(url = member.avatar_url)
#                     await ctx.send(embed=embed)
#                 else:
#                     warn_id_ref=0
#                     warn_id[server_ref].append(warn_ref)
#                     warn_number[server_ref].append(1)

#                     if not raison:
#                         warnRaison = "Aucunne raison donnée."
#                     else:
#                         warnRaison = " ".join(raison)

#                     embed = discord.Embed(title=f"Warn", description=f"Un warn a été attribué à {user}, c'est son premier warn ", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
#                     embed.add_field(name="Modérateur :", value=f" {ctx.message.author.name} ")
#                     embed.add_field(name="Joueur :", value=f" {user} ")
#                     embed.add_field(name="Raison :", value=f" {warnRaison} ")
#                     embed.add_field(name="Nombre de Warn :", value=f" 1 ")
#                     embed.set_thumbnail(url = member.avatar_url)

#                     await ctx.send(embed=embed)
#             else:
#                 server_ref=0
#                 warn_id_ref=0
#                 warn_server.append(server)
#                 warn_id.append([warn_ref])
#                 warn_number.append([1])
#                 if not raison:
#                     warnRaison = "Aucunne raison donnée."
#                 else:
#                     warnRaison = " ".join(raison)

#                 embed = discord.Embed(title=f"Warn", description=f"Un warn a été attribué à {user}, c'est son premier warn ", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
#                 embed.add_field(name="Modérateur :", value=f" {ctx.message.author.name} ")
#                 embed.add_field(name="Joueur :", value=f" {user} ")
#                 embed.add_field(name="Raison :", value=f" {warnRaison} ")
#                 embed.add_field(name="Nombre de Warn :", value=f" 1 ")
#                 embed.set_thumbnail(url = member.avatar_url)

#                 await ctx.send(embed=embed)
#             #Sanctions vérifications :
#             if warn_number[server_ref][warn_id_ref]==3:
#                 await member.edit(mute = True)
#             elif warn_number[server_ref][warn_id_ref]==6:
#                 await ctx.guild.kick(member, reason ="6 warns=kick" )
#                 await ctx.send(f"{user} à été kick.Raison : 6 warns")
#             elif warn_number[server_ref][warn_id_ref]==9:
#                 await ctx.guild.ban(member, reason ="9 warns=ban")
#                 await ctx.send(f"{user} à été ban.Raison : 9 warns ")

#     @commands.command()
#     @commands.has_permissions(ban_members = True)
#     async def warn_annulate(self, ctx,member :discord.Member):
#             global warn_server
#             global warn_id
#             global warn_number
#             server=ctx.message.guild.id
#             warn_ref=int(member.id)
#             user=str(member.name)
#             if server in warn_server:
#                 server_ref=warn_server.index(server)
#                 if warn_ref in warn_id[server_ref]:
#                     warn_id_ref=warn_id[server_ref].index(warn_ref)
#                     if warn_number[server_ref][warn_id_ref]>0:
#                         warn_number[server_ref].insert(warn_id_ref,warn_number[server_ref][warn_id_ref]-1)
#                         text="Un warn retiré à"+str(user)+", il a un total de "+str(warn_number[server_ref][warn_id_ref])+" warns"
#                         await ctx.send(text)
#                     else:
#                         await ctx.send("Erreur, cet utilisateur n'a pas de warn, en annuler un est donc impossible")
#                 else:
#                     await ctx.send("Erreur, cet utilisateur n'a reçu aucun warn, en annuler un est donc impossible")
#             else:
#                 await ctx.send("Erreur, ce serveur n'a attribué encore aucun warn, en annuler un est donc impossible")

#     @commands.command()
#     @commands.has_permissions(ban_members = True)
#     async def warn_clear(self, ctx,member :discord.Member):
#             global warn_server
#             global warn_id
#             global warn_number
#             server=ctx.message.guild.id
#             warn_ref=int(member.id)
#             user=str(member.name)
#             if server in warn_server:
#                 server_ref=warn_server.index(server)
#                 if warn_ref in warn_id[server_ref]:
#                     warn_id_ref=warn_id[server_ref].index(warn_ref)
#                     warn_number[server_ref].insert(warn_id_ref,0)
#                     text="Les warns de "+str(user)+" ont été clear, il a un total de "+str(warn_number[server_ref][warn_id_ref])+" warns désormais"
#                     await ctx.send(text)
#                 else:
#                     await ctx.send("Erreur, cet utilisateur n'a reçu aucun warn, clear ses warns est donc impossible")
#             else:
#                 await ctx.send("Erreur, ce serveur n'a attribué encore aucun warn, clear les warns de quelqu'un est donc impossible")