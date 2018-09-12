import error_handler
from discord.ext import commands
import config
from elasticsearch import Elasticsearch

bot = commands.Bot(command_prefix=['?', '!', '/'], description="jake and amir bot!")
bot.add_cog(error_handler.CommandErrorHandler(bot))
es = Elasticsearch()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def search(*, quote):
    search_res = es.search(index="ja-test_index",
                           body={"query": {"match": {"script": {"query": quote, "fuzziness": "AUTO"}}}})
    elasticsearch_hits = search_res['hits']['hits']

    if elasticsearch_hits:
        await bot.say(elasticsearch_hits[0]['_source']['link'])
    else:
        await bot.say("Sorry, couldn't find an episode for that quote.")

bot.run(config.discord_token)
