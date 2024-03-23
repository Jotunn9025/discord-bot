import discord
import config
from discord.ext import commands
import time

intents = discord.Intents.all()
client = discord.Client(intents=intents)

command_line_ranges = {
    "~peppa": slice(0, 11), 
    "~kanthulu": slice(12, 24),
    "~millet": slice(25, 43),
    "~draconis": slice(44,55),
    "~dory":slice(56,69),
    "~help":slice(70,75),
}

last_execution_times = {}

@client.event
async def on_ready():
    print("I'm up and running, boss")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    for command, line_range in command_line_ranges.items():
        if message.content.startswith(command):
            current_time = time.time()
            last_exec_time = last_execution_times.get((message.author.id, command), 0)
            if current_time - last_exec_time > 60:
                last_execution_times[(message.author.id, command)] = current_time
                
                peppa_str = ""
                with open("peppa.txt", "r") as fp:
                    lines = fp.readlines()
                    for line in lines[line_range]:
                        peppa_str += line
                await message.channel.send(peppa_str)
            else:
                await message.channel.send("You can only use this command once per minute.")
            break 

client.run(config.DISCORD_TOKEN)
