from keep_alive import keep_alive
keep_alive()

import discord
from discord.ext import commands

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

bot.run(TOKEN)
