import discord
import error_handler
from discord.ext import commands
import config

bot = commands.Bot(command_prefix=['?', '!'], description="jake and amir bot!")
bot.add_cog(error_handler.CommandErrorHandler(bot))
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping():
    await bot.say("pong!")

@bot.command()
async def search(*, input):
    await bot.say("you searched " + input)

bot.run(config.token)
