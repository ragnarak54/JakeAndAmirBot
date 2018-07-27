import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=['?', '!'], description="jake and amir bot!")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping():
    await bot.say("pong!")

bot.run('NDcyMjE5ODgxNTc2NzI2NTYw.DjwOYA.AZU_f1dEB4eXQ9nrLZEieri_k0I')