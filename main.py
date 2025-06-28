import os
import discord
from discord.ext import commands

TOKEN = os.environ['TOKEN']  # Render 환경변수에서 불러오기
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

bot.run(TOKEN)
