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
import glob
import os
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

bot = commands.Bot(command_prefix = f"{config['prefix']}", intents=intents, help_command=None)

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

    # Load de Commands
    for files in os.listdir(path + '/commands'):

        if files != "__pycache__":
            if os.path.isdir(path + '/commands/' + files):
                folder = path + '/commands/' + files
                for command_file in os.listdir(folder):
                    if command_file != "__pycache__":

                        try:
                            bot.reload_extension(f"commands.{files}." + command_file[:-3])
                        except:
                            bot.load_extension(f"commands.{files}." + command_file[:-3])
        
        if os.path.isfile(path + "/commands/" + files):
            try:
                bot.reload_extension("commands." + files[:-3])
            except:
                bot.load_extension("commands." + files[:-3])
        
    # Load d'event
    for files in os.listdir('events'):
        if(files != "__pycache__"):
            try:
                bot.reload_extension("events." + files[:-3])
            except:
                bot.load_extension("events." + files[:-3])

#######################################################################################
# Event
#######################################################################################


# on_message Event 
# @params : message
@bot.event
async def on_message(message):

    with open(path + '/json/channel.json') as data:
        channel = json.load(data)

    if message.author == bot.user:
        return
      
    for sc in channel['suggestion']['channel']:
        if message.channel.id == int(sc):
            await message.add_reaction('✅')
            await message.add_reaction('❌')

    for ac in channel['annonce']['channel']:
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

    for var in hello_variable:
        if message.content.startswith(var):
            await message.add_reaction('👋')

    await bot.process_commands(message)

#######################################################################################
# Reload command
####################################################################################### 

@bot.command()
@commands.check(isOwner)
async def reload(ctx):
    commands_list = os.listdir('commands')
    for files in commands_list:
        if(files != "__pycache__"):
                
            try:
                bot.reload_extension("commands." + files[:-3])
            except:
                bot.load_extension("commands." + files[:-3])

bot.run(config['token'])