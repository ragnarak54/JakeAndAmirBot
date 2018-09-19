import error_handler
from discord.ext import commands
import config
import ES

bot = commands.Bot(command_prefix=['?', '!', '/'], description="jake and amir bot!")
bot.add_cog(error_handler.CommandErrorHandler(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def search(*, quote):
    elasticsearch_hit = ES.search_script(quote)

    if elasticsearch_hit:
        await bot.say(elasticsearch_hit['_source']['youtube_link'])
    else:
        await bot.say("Sorry, couldn't find an episode for that quote.")

bot.run(config.discord_token)
