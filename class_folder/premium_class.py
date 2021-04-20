import random
import requests
import discord
import os
import json

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

class Premium_Class():

    async def check_premium(self, ctx):
        find = 0

        with open(path + '/json/roles.json') as data:
            pre = json.load(data)

        for role in ctx.message.author.roles:
            for p in pre['premium']:
                if p == role.id:
                    find += 1
        
        if find == 0:
            await ctx.send("Vous n'êtes pas premium.")
            return
    
    async def check_author_voc(self, ctx, channel_id):
        with open(path + '/json/voc.json') as data:
            voc_json = json.load(data)

        if channel_id in voc_json['voc']['voc_id']:
            index = voc_json['voc']['voc_id'].index(channel_id)
            if voc_json['voc']['author_id'][index] != ctx.message.author.id:
                return await ctx.send("Vous n'êtes pas l'autheur de se channel.")
        else:
            return await ctx.send('Vous ne pouvez pas exécuter la commande dans se channel.')