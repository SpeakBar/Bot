import discord
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions

import datetime
import time

import asyncio
import random
import requests
import re

import json
import os.path
from os import path

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

with open(path + '/config.json') as data:
    config = json.load(data)

hello_variable = [
    "Salut",
    "salut",
    "Hello",
    "hello",
    "Hi",
    "hi",
    "Yo",
    "yo",
    "bjr",
    "Bonjour",
    "bonjour"
    "Hey",
    "hey"
]

intents = discord.Intents().all()

bot = commands.Bot(command_prefix = f"{config['prefix']}", descriptions = "", intents=intents, help_command=None)

def isOwner(ctx):
    for owner_bot in config['owner_id']:
        return ctx.message.author.id == int(owner_bot)

@bot.event
async def on_ready():
    if 'on_ready' in config:
        print(config['on_ready'])
    else:
        print("ready")
    
    await bot.change_presence(status = discord.Status.online ,activity=discord.Game("Speakbar.fr"))
    
    #Voc init
    global voc_id
    voc_id=[]
    global voc_user
    voc_user=[]

    # Warn
    global warn_server
    warn_server=[]
    global warn_id
    warn_id=[]
    global warn_number
    warn_number=[]

#######################################################################################
# Event
#######################################################################################


# on_message Event 
# @params : message
@bot.event
async def on_message(message):

    with open(path + '/json/dashboard.json') as data:
        dashboard = json.load(data)

    if message.author == bot.user:
        return
      
    for sc in dashboard['suggestion_channel']:
        if message.channel.id == int(sc):
            await message.add_reaction('✅')
            await message.add_reaction('❌')

    for ac in dashboard['annonce_channel']:
        if message.channel.id != int(ac):
            if re.findall('https://discord.gg/[a-zA-Z0-9]', message.content):
                await message.delete()

            elif re.findall('http://discord.gg/[a-zA-Z0-9]', message.content):
                await message.delete()

            elif re.findall('https://discord.com/invite/[a-zA-Z0-9]', message.content):
                await message.delete()

            elif re.findall('http://discord.com/invite/[a-zA-Z0-9]', message.content):
                await message.delete()

    if message.content.startswith('prefix'):
        await message.channel.send('Voila mon prefix : **' + bot.command_prefix + '**')
    
    if bot.user.mentioned_in(message):
        await message.channel.send("Faites `"+bot.command_prefix+"help` pour connaitre mais commandes.")

    for var in hello_variable:
        if message.content.startswith(var):
            await message.add_reaction('👋')

    await bot.process_commands(message)

# on_reaction_add Event 
# @params : reaction, user
@bot.event
async def on_reaction_add(reaction, user):

    with open(path + '/json/dashboard.json') as data:
        dashboard = json.load(data)
    with open(path + '/json/bdd.json') as data:
        bdd = json.load(data)

    if reaction.message.author == bot.user:
        return
    
    if reaction.emoji == '🌟':
        if reaction and reaction.count == 1:
            for bs in bdd['stars_message']:
                if int(bs) == reaction.message.id:
                    return

            server = bot.get_guild(reaction.message.guild.id)
            for c in dashboard['stars_channel']:
                if server.get_channel(int(c)):

                    channel = server.get_channel(int(c))

                    # Embed
                    embed = discord.Embed(title=f"5 🌟" ,description=reaction.message.content, timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
                    embed.set_footer(icon_url = reaction.message.author.avatar_url, text=reaction.message.author.name)

                    await channel.send(embed=embed)

            ############# BDD ##############
            bdd['stars_message'].append(f'{reaction.message.id}')

            y = json.dumps(bdd)

            f = open(path + "/json/bdd.json", "w")
            f.write(y)
            f.close()
            ############# BDD ##############

            await reaction.message.pin(reason="rien")
            # await reaction.message.add_reaction('🌟')

@bot.event
async def on_voice_state_update(member, before, after):
    global voc_id
    global voc_user
    with open(path + '/json/voc.json') as data:
        voc = json.load(data)
    
    guild = bot.get_guild(member.guild.id)
    for mc in voc['music_channel']:
        music_channel = bot.get_channel(int(mc))

    if before.channel==None and after.channel is not None:
        for vc in voc['voc_channel']:
            if after.channel.id==int(vc): #Si on arrive dans un channel de création (Voc de Nirbose)
                if not member in voc_user: # Si cette personne n'a pas déjà crée un vocal
                    for vcc in voc['voc_category']:
                        category = bot.get_channel(int(vcc))

                    await guild.create_voice_channel(f"🍺-Voc de {member.name}", category=category) #, overwrites=None, category=category, reason=None  pour détailler catégorie et autres ici cas défaut donc même catégorie ^^
                    #Move du créateur du salon :
                    for channel in guild.channels:
                        if channel.name == f"🍺-Voc de {member.name}" :
                            print("VOCAL_Construction pour",member)
                            wanted_channel_id = channel.id
                            voc_id.append(wanted_channel_id)
                            voc_user.append(member)
                            await member.move_to(channel)
        try:
            await music_channel.set_permissions(member, view_channel=True, send_messages=True)
        except:
            pass

                        
    else:
        if before.channel.id in voc_id:
            if len(before.channel.members)==0:
                #Destruction du channel si il n'y a plus personne
                print("VOCAL_Destruction")
                index = voc_id.index(before.channel.id)
                del voc_id[index]
                del voc_user[index]
                await before.channel.delete()
        try:
            await music_channel.set_permissions(member, view_channel=False, send_messages=False)
        except:
            pass

#######################################################################################
# Commands
####################################################################################### 


@bot.command()
@commands.check(isOwner)
async def load(ctx, name=None, description="Returns all commands available"):
    if name:
        bot.load_extension("commands." + name)
        await ctx.send('Fichier load.')


@bot.command()
@commands.check(isOwner)
async def unload(ctx, name=None, description="Returns all commands available"):
    if name:
        bot.unload_extension ("commands." + name)
        await ctx.send('Fichier unload.')


@bot.command()
@commands.check(isOwner)
async def reload(ctx, name=None, description="Returns all commands available"):
    if name:
        try:
            bot.reload_extension("commands." + name)
            await ctx.send('Fichier reload.')
        except:
            bot.load_extension("commands." + name)
            await ctx.send('Fichier load.')

@bot.command()
@commands.check(isOwner)
async def all_load(ctx):
    with open('cogs.json') as data:
        cog = json.load(data)
    
    for c in cog['cogs']:
        try:
            bot.reload_extension("commands." + c)
        except:
            bot.load_extension("commands." + c)
    await ctx.send('Tout les fichier sont load | reload')

bot.run(config['token'])