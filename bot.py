import discord
import config
from discord.ext import commands
import time
import random
intents = discord.Intents.all()
client = discord.Client(intents=intents)

command_line_ranges = {
    "~peppa": slice(0, 11), 
    "~kanthulu": slice(12, 24),
    "~millet": slice(25, 43),
    "~draconis": slice(44,55),
    "~dory":slice(56,69),
    "~help":slice(70,76),
    "~r":slice(0,0),
}

last_execution_times = {}

@client.event
async def on_ready():
    print("I'm up and running, boss")
    config.thanks_count = load_thanks_count()  # Load thanks count from file when the bot starts

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    for command, line_range in command_line_ranges.items():
        if message.content.startswith(command):
            current_time = time.time()
            last_exec_time = last_execution_times.get((message.author.id, command), 0)
            cooldown = 5 if command in ["~r","~help"] else 60
            if current_time - last_exec_time > cooldown:
                last_execution_times[(message.author.id, command)] = current_time
                
                if command == "~r":
                    try:
                        args = message.content.split()[1:]
                        if len(args) != 1:
                            await message.channel.send("Invalid format. Please use: ~r [number of dice]d[number of faces]")
                            return
                        num_dice, num_faces = map(int, args[0].split('d'))
                        if num_dice > 20 or num_faces > 20:
                            await message.channel.send("You can only roll up to 20 dice or 20 faces.")
                            return
                        rolls = [random.randint(1, num_faces) for _ in range(num_dice)]
                        total = sum(rolls)
                        await message.channel.send(f"Rolls: {' '.join(map(str, rolls))}\nTotal: {total}")
                    except ValueError:
                        await message.channel.send("Invalid format. Please use: ~r [number of dice]d[number of faces]")
                else:
                    peppa_str = ""
                    with open("peppa.txt", "r") as fp:
                        lines = fp.readlines()
                        for line in lines[line_range]:
                            peppa_str += line
                    await message.channel.send(peppa_str)
            else:
                await message.channel.send(f"You can only use this command once every {cooldown} seconds.")
            break 
    
    if "good bot" in message.content.lower() and message.author != client.user:
        config.thanks_count += 1
        await message.channel.send(f"Thanks\nThanks count: {config.thanks_count}")
        save_thanks_count(config.thanks_count)  # Save thanks count to file

def load_thanks_count():
    try:
        with open("thanks_count.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_thanks_count(count):
    with open("thanks_count.txt", "w") as file:
        file.write(str(count))

client.run(config.DISCORD_TOKEN)

