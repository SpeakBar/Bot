import discord
from discord.ext import commands, tasks
import datetime
import time
import random
import os

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

def setup(bot):
    bot.add_cog(Giveaway(bot))

#Chargement Giveaway
global giveaway_type
giveaway_type=[]
global giveaway_time
giveaway_time=[]
global giveaway_id
giveaway_id=[]
global giveaway_channel
giveaway_channel=[]
global giveaway_message
giveaway_message=[]
fichier=open(path + "/giveaway.txt",mode="r",encoding="utf8")
ligne=[]
for lines in fichier:
    ligne.append(lines)
if len(ligne)>4:
    #Type
    liste=ligne[0].split("//_giveawaySecurity2000ofhacking_//")
    maxdata=len(liste)
    count=0
    for data in liste:
        count+=1
        if count<maxdata:
            giveaway_type.append(str(data))
        else:
            giveaway_type.append(str(data[:-1]))
    #Time
    liste=ligne[1].split("//_giveawaySecurity2000ofhacking_//")
    for data in liste:
        liste3=[]
        liste2=data.split("//_giveaway_data_list_security_//")
        for data2 in liste2:
            liste3.append(int(data2))
        giveaway_time.append(liste3)
    #ID
    liste=ligne[2].split("//_giveawaySecurity2000ofhacking_//")
    for data in liste:
        giveaway_id.append(int(data))
    #Channel
    liste=ligne[3].split("//_giveawaySecurity2000ofhacking_//")
    for data in liste:
        giveaway_channel.append(int(data))#str or int ?
    #Messages
    liste=ligne[4].split("//_giveawaySecurity2000ofhacking_//")
    for data in liste:
        giveaway_message.append(int(data))
fichier.close()

class Giveaway(commands.Cog):

    def giveawayPerm(ctx):
        return ctx.message.author.id == 549592568694833152

    def __init__(self, bot):
        self.bot = bot
        self.giveaway_check.start()
        global giveaway_type
        giveaway_type=[]
        global giveaway_time
        giveaway_time=[]
        global giveaway_id
        giveaway_id=[]
        global giveaway_channel
        giveaway_channel=[]
        global giveaway_message
        giveaway_message=[]

    @commands.command()
    @commands.check(giveawayPerm)
    async def giveaway(self,ctx,title, date):
            #Init
            global giveaway_id
            global giveway_time
            global giveaway_type
            global giveaway_channel
            global giveaway_message
            FinalT=date.split("/")
            embed = discord.Embed(title="Giveaway"+":tada:", description="Cliquez sur la réaction avant la fin du temps pour participer", timestamp=datetime.datetime.utcnow(), color=discord.Colour(int("FFD51A", 16)))
            embed.add_field(name=":gift:"+"Giveaway pour :",value=title)
            embed.add_field(name=":stopwatch:"+"Fin du giveaway à :",value="Le "+str(FinalT[0])+"/"+str(FinalT[1])+"/"+str(FinalT[2])+" à "+str(FinalT[3])+"h"+str(FinalT[4]))
            message=await ctx.send(embed=embed)
            await message.add_reaction("✅")
            giveaway_message.append(message.id)
            giveaway_id.append(len(giveaway_id)+1)
            giveaway_type.append(title)
            giveaway_time.append(FinalT)
            giveaway_channel.append(ctx.channel.id)
            giveaway_save()
    @tasks.loop(seconds = 5)
    #Vérification
    async def giveaway_check(self):
            global giveaway_id
            global giveway_time
            global giveaway_type
            global giveaway_channel
            global giveaway_message
            Temps=time.localtime()
            count=0
            for idgive in range(0,len(giveaway_id)):
                end=0
                idgive=idgive-count
                print(idgive)
                print(count)
                limit=giveaway_time[idgive-1]
                if int(Temps[0])>int(limit[2]):
                    end=1
                elif int(Temps[0])==int(limit[2]):
                    if int(Temps[1])>int(limit[1]):
                        end=1
                    elif int(Temps[1])==int(limit[1]):
                        if int(Temps[2])>int(limit[0]):
                            end=1
                        elif int(Temps[2])==int(limit[0]):
                            if int(Temps[3])>int(limit[3]):
                                end=1
                            elif int(Temps[3])==int(limit[3]):
                                if int(Temps[4])>int(limit[4])-1:
                                    end=1
                #Si giveaway terminé :
                if end==1:
                    count=count+1
                    print("Giveaway terminé")
                    channel = self.bot.get_channel(giveaway_channel[idgive-1])

                    await channel.send('Giveaway terminé, Résultats du tirage !')
                    
                    #Tirage
                    allWhoReacted = []
                    messageID=giveaway_message[idgive-1]
                    ChannelID=giveaway_channel[idgive-1]
                    serverID=""
                    message = await channel.fetch_message(messageID)
                    allReactions = message.reactions
                    for reaction in allReactions:
                            #print(str(reaction.emoji))
                            if str(reaction.emoji) == "✅":
                                    async for user in reaction.users():
                                            if not user == self.bot.user:
                                                    if not user in allWhoReacted:
                                                            allWhoReacted.append(user)
                    print(allWhoReacted)
                    if len(allWhoReacted)>0:
                            gagnant=random.choice(allWhoReacted)
                            text="Le gagnant est "+str(gagnant)
                            await channel.send(text)
                    else:
                            await channel.send('Aucun gagnant, faute de participants ...') 
                    del(giveaway_id[idgive-1])
                    del(giveaway_type[idgive-1])
                    del(giveaway_time[idgive-1])
                    del(giveaway_channel[idgive-1])
                    del(giveaway_message[idgive-1])
                    giveaway_save()

def giveaway_save():
    fichier=open(path + "/giveaway.txt",mode="w",encoding="utf8")
    fichier.write("//_giveawaySecurity2000ofhacking_//".join(giveaway_type)+"\n")
    maxdata=len(giveaway_time)
    count=0
    for data in giveaway_time:
        count+=1
        maxdata2=len(data)
        count2=0
        for data2 in data:
            count2+=1
            if count2<maxdata2:
                fichier.write(str(data2)+"//_giveaway_data_list_security_//")
            else:
                fichier.write(str(data2))
        if count<maxdata:
            fichier.write("//_giveawaySecurity2000ofhacking_//")
        else:
            fichier.write("\n")
    
    #OK
    maxdata=len(giveaway_id)
    count=0
    for data in giveaway_id:
        count+=1
        if count<maxdata:
            fichier.write(str(data)+"//_giveawaySecurity2000ofhacking_//")
        else:
            fichier.write(str(data)+"\n")
    maxdata=len(giveaway_channel)
    count=0
    for data in giveaway_channel:
        count+=1
        if count<maxdata:
            fichier.write(str(data)+"//_giveawaySecurity2000ofhacking_//")
        else:
            fichier.write(str(data)+"\n")
    maxdata=len(giveaway_message)
    count=0
    for data in giveaway_message:
        count+=1
        if count<maxdata:
            fichier.write(str(data)+"//_giveawaySecurity2000ofhacking_//")
        else:
            fichier.write(str(data)+"\n")
    fichier.close()
    print("SAUVEGARDE DONNEES SERVEUR GIVEAWAY EFFECTUEE")
