import discord
from discord.ext import commands
from discord import Permissions
import time, requests, os, sys
from discord import File
import os
import time
import json
import random
import locale
import threading
import socket
import openai
import re


def format_number(number):
    return "{:,}".format(number)

token = "tokengir"
intents = discord.Intents().all()
client = commands.Bot(command_prefix="t",intents=intents)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    myUrl = "https://discord.com/api/webhooks/1065211364894838814/qk7hMI4F6q9ulJKrmCrEkHqxQaRuvaBeg1ZhbiwrMcdv_IYBRKvShHPak3rPhg6TiDlV"

    data2 = {"content":"Bot başarılı şekilde aktif... @here "}
    responsed = requests.post(myUrl, json=data2)

    print(responsed.status_code)

    print(responsed.content)
 
# Verileri saklamak için bir JSON dosyası oluşturun
data = {"para": []}

with open("veriler.json", "w") as file:
    json.dump(data, file)

# Verileri eklemek için
data_lock = threading.Lock()

def add_data(para):
    with data_lock:
        with open("veriler.json", "r") as file:
            data = json.load(file)
        data["para"].append(para)
        with open("veriler.json", "w") as file:
            json.dump(data, file)

def read_data():
    with data_lock:
        with open("veriler.json", "r") as file:
            data = json.load(file)
    return data["para"]







# Örnek kullanım
add_data("9999")

data = {"para": []}
with open("veriler.json", "w") as file:
    json.dump(data, file)

@client.command()
async def money(ctx):
    with open("veriler.json", "r") as json_file:
        data = json.load(json_file)
    if not data["para"]:
        await ctx.send("Your tcash money is 0")
    else:
        money = sum(data["para"])
        formatted_money = format_number(money)
        await ctx.send("Your tcash money is " + formatted_money)


    

 
    
@client.command()
async def kumar(ctx):
    kumar = random.randint(0,1)
    if kumar == 1:
        random_money = random.randint(1000,10000)
        with open("veriler.json", "r") as json_file:
            data = json.load(json_file)
            data["para"].append(random_money)
        with open("veriler.json", "w") as json_file:
            json.dump(data, json_file)
        await ctx.send("You won! Your tcash money is " + str(random_money))
    else:
        await ctx.send("You lose! Your tcash money is still the same.")




@client.command(name="yardım")
async def help_command(ctx):
    embed = discord.Embed(
        title="Bot Yardım",
        description="Aşağıdaki komutlar mevcuttur:",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1064793632319754291/64bf88a0d71f905e116ebdcc973469af.webp?size=80")

    for command in client.commands:
        embed.add_field(name=f"{client.command_prefix}{command.name}", value=command.help, inline=False)

    await ctx.send(embed=embed)
@client.command()
async def kanalaç(ctx, channel_name:str):
    guild = ctx.guild
    await guild.create_text_channel(channel_name)
    await ctx.send(f"{channel_name} kanalı oluşturuldu!")
@client.command()
async def kanaloluştur(ctx, channel_name:str, channel_count:int):
    guild = ctx.guild
    for i in range(channel_count):
        await guild.create_text_channel(f"{channel_name}-{i+1}")
    await ctx.send(f"{channel_count} adet {channel_name} kanalı oluşturuldu!")
@client.command()
async def kanalsil(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    channel_name = "DELETED"
    channel2= await guild.create_text_channel(channel_name)     
    await channel2.send("Tüm kanallar silindi!")
@client.command()
async def ban(ctx, member: discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} yasaklandı.")
@client.command()
async def kick(ctx, member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} sunucudan atıldı.")
@client.command()
async def ping(ctx, website):
    try:
        r = requests.get(website)
        await ctx.send(f'{website} üzerinden ping: {r.elapsed.microseconds / 1000} ms')
    except:
        await ctx.send("Hata oluştu, lütfen geçerli bir web sitesi girin")


@client.command()
async def kontrol(ctx, website: str):
    r = requests.get(website)
    if r.status_code =="200":
        await ctx.reply("STATUS CODE İS : 200 SİTE AKTİF.")
        ip = os.popen(f'ping {website} -c 1').read().split()[-2]
        await ctx.send(f'{website} website\'s IP address: {ip}')
    else:
        await ctx.reply("SİTE KAPALI")
        await ctx.reply("STATUS CODE:")
        await ctx.send(r.status_code)
        r = requests.get(website)
        await ctx.send(f'{website} Site pingi: {r.elapsed.microseconds / 1000} ms')
    
        
@client.command()
async def scan_ports(ctx, host:str):
    open_ports = []
    for port in range(1, 65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
    with open("open_ports.txt", "w") as file:
        file.write("Open ports on {}:".format(host))
        for port in open_ports:
            file.write("\n" + str(port))
    await ctx.send(file=File("open_ports.txt"))
    

    




@client.command()
async def get_html(ctx, url:str):
    page = requests.get(url)
    with open("page.txt", "w") as file:
        file.write(page.text)
    await ctx.send(file=File("page.txt"))

openai.api_key = "AİKEY"

@client.command(name='chat')
async def chat(ctx, *, message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{message}"
    )
    text = response.choices[0].text
    await ctx.send(text)

@client.command()
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f"{member.name} için bilgi", color=discord.Color.blue())
    embed.add_field(name="Kullanıcı adı", value=member.name, inline=True)
    embed.add_field(name="Kullanıcı ID", value=member.id, inline=True)
    embed.add_field(name="Hesap açılış tarihi", value=member.created_at.strftime("%d %B %Y %H:%M"), inline=True)
    embed.add_field(name="Sunucuya giriş tarihi", value=member.joined_at.strftime("%d %B %Y %H:%M"), inline=True)
    embed.add_field(name="Rol", value=member.top_role, inline=True)
    await ctx.send(embed=embed)
import time

# Spam korumasını etkinleştir
spam_protection = True

# Kullanıcının son mesajını gönderdiği zaman
last_message_time = {}

# Kullanıcının son mesajının içeriği
last_message_content = {}

@client.event
async def on_message(message):
    # Spam koruması etkinleştirilmişse
    if spam_protection:
        # Kullanıcının son mesajını gönderdiği zamanı al
        current_time = time.time()
        if message.author in last_message_time:
            last_message_time_user = last_message_time[message.author]
            last_message_content_user = last_message_content[message.author]
        else:
            last_message_time_user = 0
            last_message_content_user = ""
        
        # Kullanıcının son mesajının içeriğini ve zamanını kontrol et
        if (current_time - last_message_time_user < 60) and (last_message_content_user == message.content):
            # Kullanıcının mesajını sil
            await message.delete()
            # Kullanıcıya uyarı gönder
            await message.channel.send(f"{message.author.mention} spam yapmayın!")
        else:
            # Kullanıcının son mesajının zamanını ve içeriğini kaydet
            last_message_time[message.author] = current_time
            last_message_content[message.author] = message.content
import re

# Küfür kelimelerinin listesi
profanity = ["amk", "mal", "oç","orospu","aq","Amk", "Mal", "Oç","Orospu","Aq","Ananı","ananı","sikiş","Sikiş"]

@client.event
async def on_message(message):
    # Mesajı kontrol et
    for word in profanity:
        if re.search(word, message.content, re.IGNORECASE):
            # Kullanıcının mesajını sil
            await message.delete()
            # Kullanıcıya uyarı gönder
            await message.channel.send(f"{message.author.mention} Küfür yasaktır!")
            break


# Spam korumasını etkinleştir
spam_protection = True

# Kullanıcının son mesajını gönderdiği zaman
last_message_time = {}

# Kullanıcının son mesajının içeriği
last_message_content = {}

# Kullanıcının ban sayısı
ban_count = {}

@client.event
async def on_message(message):
    # Spam koruması etkinleştirilmişse
    if spam_protection:
        # Kullanıcının son mesajını gönderdiği zamanı al
        current_time = time.time()
        if message.author in last_message_time:
            last_message_time_user = last_message_time[message.author]
            last_message_content_user = last_message_content[message.author]
            ban_count_user = ban_count.get(message.author, 0)
        else:
            last_message_time_user = 0
            last_message_content_user = ""
            ban_count_user = 0
        
        # Kullanıcının son mesajının içeriğini ve zamanını kontrol et
        if (current_time - last_message_time_user < 60) and (last_message_content_user == message.content):
            # Kullanıcının mesajını sil
            await message.delete()
            ban_count_user += 1
            ban_count[message.author] = ban_count_user
            # Kullanıcıya uyarı gönder
            await message.channel.send(f"{message.author.mention} spam yapmayın! {ban_count_user}/3")
        else:
            # Kullanıcının son mesajının zamanını ve içeriğini kaydet
            last_message_time[message.author] = current_time
            last_message_content[message.author] = message.content
            ban_count[message.author] = 0
        if ban_count_user >= 3:
            # kullanıcıyı banla
            await message.guild.ban(message.author)
            await message.channel.send(f"{message.author.mention} 3 kere spam yaptığı için banlandı!")
@client.command()
async def jail(ctx, member: discord.Member):
    jail_role = discord.utils.get(ctx.guild.roles, name="jail")
    await member.add_roles(jail_role)
    await ctx.send(f"{member.mention} hapis edildi.")


client.run(token)
