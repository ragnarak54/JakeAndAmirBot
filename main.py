import discord
import error_handler
from discord.ext import commands
import config
from elasticsearch import Elasticsearch

bot = commands.Bot(command_prefix=['?', '!'], description="jake and amir bot!")
bot.add_cog(error_handler.CommandErrorHandler(bot))
es = Elasticsearch()

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
async def search(*, search_str):
    await bot.say("you searched " + search_str)
    search_res = es.search(index="ja-test_index",
                           body={"query": {"match": {"script": {"query": search_str, "fuzziness": "AUTO"}}}})
    for hit in search_res['hits']['hits']:
        await bot.say(hit['_source']['link'])

bot.run(config.token)
