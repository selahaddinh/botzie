import urllib.request
import json
import datetime
import discord
import asyncio

client = discord.Client()

players=[]


channelID="";
start=0;

def initialLeaderBoard():
    message=""
    now = datetime.datetime.now()
    message=now.__str__()+"\n";
    with urllib.request.urlopen("http://www.dota2.com/webapi/ILeaderboard/GetDivisionLeaderboard/v0001?division=europe") as url:
        data = json.loads(url.read().decode())
    #print(data['leaderboard'])
    leaderboard=data['leaderboard'];
    rank=0;
    found=0;
    for x in leaderboard:
        rank=rank+1;
        if (x['name']==players[len(players)-1]):
                print(x)
                found=1;
                print(rank)
                message=str(x)+" rank: "+rank.__str__()+"\n";


    if found==0:
        message="No player found with name "+players[len(players)-1]+" check for capital letters etc";
    return message




def getLeaderboard():
    message=""
    now = datetime.datetime.now()
    message=now.__str__()+"\n";
    with urllib.request.urlopen("http://www.dota2.com/webapi/ILeaderboard/GetDivisionLeaderboard/v0001?division=europe") as url:
        data = json.loads(url.read().decode())
    #print(data['leaderboard'])
    leaderboard=data['leaderboard'];
    rank=0;
    for x in leaderboard:
        rank=rank+1;
        for i in players:
            if (x['name']==i):
                print(x)

                print(rank)
                message=message+x['name']+" "+rank.__str__()+"\n";


    return message



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):

    channel = str(message.channel.id)
    command = str(message.content)
    if command.startswith("/commands"):
        commands="```Hello my name is botzie, \nMade by Knight Of Dol Amroth to serve his friends \nMy commands are: \n/start schedules me to send mmr everyday " \
                 "\n/mmr which makes me show mmr of players on my list \n/add which adds players to my list```"
        await client.send_message(message.channel, commands)


    if command.startswith("/start"):
        global channelID
        channelID=message.channel.id;
        global start
        start=1

    if command.startswith("/mmr"):
        getLeaderboard()
        if len(players)!=0:
            await client.send_message(message.channel, "```"+getLeaderboard()+"```")
        else:
            await client.send_message(message.channel, "```"+getLeaderboard()+ "\n" +"No players in list"+"```")

    if command.startswith("/add"):
        command = command.replace("/add ", "")
        if command == "":
            await client.send_message(message.channel, "```:x: No player entered.```")
            print(":x: No player entered.")
        else:
            player=command
            players.append(player)
            playerinfo=initialLeaderBoard()

            await client.send_message(message.channel, "```player "+player+" added \n"+playerinfo+"```")



async def my_background_task():
    await client.wait_until_ready()


    while not client.is_closed:
        if start==1:
            channel = discord.Object(id=channelID)
            counter = getLeaderboard()
            await client.send_message(channel, counter)

        await asyncio.sleep(60*60*24) # task runs every day



client.loop.create_task(my_background_task())
client.run('token')
