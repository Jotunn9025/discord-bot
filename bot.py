import discord
import config
from discord.ext import commands
intents=discord.Intents.all()
client=discord.Client(intents=intents)

@client.event
async def on_ready():
    print("im up and running, boss")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("`youhan is kool"):
        await message.channel.send("pls save me this is not of my volit...aaaah")
        
client.run(config.DISCORD_TOKEN)