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
    bot.add_cog(Voice_event(bot))

class Voice_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        global voc_id
        voc_id=[]
        global voc_user
        voc_user=[]
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open(path + '/json/voc.json') as data:
            voc_json = json.load(data)
        global voc_id
        global voc_user
        with open(path + '/json/channel.json') as data:
            voc = json.load(data)
        
        guild = self.bot.get_guild(member.guild.id)
        for mc in voc['vocal']['music_channel']:
            music_channel = self.bot.get_channel(int(mc))

        if before.channel==None and after.channel is not None:
            for vc in voc['vocal']['create_channel_main']:
                if after.channel.id==int(vc): #Si on arrive dans un channel de création (Voc de Nirbose)
                    if not member in voc_json['voc']['author_id']: # Si cette personne n'a pas déjà crée un vocal
                        for vcc in voc['vocal']['category']:
                            category = self.bot.get_channel(int(vcc))

                        await guild.create_voice_channel(f"🍺-Voc de {member.name}", category=category) #, overwrites=None, category=category, reason=None  pour détailler catégorie et autres ici cas défaut donc même catégorie ^^
                        #Move du créateur du salon :
                        for channel in guild.channels:
                            if channel.name == f"🍺-Voc de {member.name}" :
                                print("VOCAL_Construction pour",member)
                                wanted_channel_id = channel.id
                                voc_json['voc']['voc_id'].append(wanted_channel_id)
                                voc_json['voc']['author_id'].append(member.id)

                                with open(path + '/json/voc.json', 'w') as data:
                                    json.dump(voc_json, data)
                                
                                await member.move_to(channel)
            try:
                await music_channel.set_permissions(member, view_channel=True, send_messages=True)
            except:
                pass

                            
        else:
            if before.channel.id in voc_json['voc']['voc_id']:
                if len(before.channel.members)==0:
                    #Destruction du channel si il n'y a plus personne
                    print("VOCAL_Destruction")
                    index = voc_json['voc']['voc_id'].index(before.channel.id)
                    del voc_json['voc']['voc_id'][index]
                    del voc_json['voc']['author_id'][index]
                    with open(path + '/json/voc.json', 'w') as data:
                        json.dump(voc_json, data)
                    await before.channel.delete()
            try:
                await music_channel.set_permissions(member, view_channel=False, send_messages=False)
            except:
                pass