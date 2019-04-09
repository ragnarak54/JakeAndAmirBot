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
async def search(ctx, *, quote):
    elasticsearch_hit = ES.search_script(quote)

    if elasticsearch_hit and '_source' in elasticsearch_hit:
        await ctx.send(elasticsearch_hit['_source']['youtube_link'] + "\n" + elasticsearch_hit['_source']['reddit_link'])
    else:
        await ctx.send("Sorry, couldn't find an episode for that quote.")

bot.run(config.discord_token)
