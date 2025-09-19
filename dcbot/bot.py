import discord
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from keep_alive import keep_alive

import os

# Set your bot token and channel ID
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Replace with your bot token
CHANNEL_ID = 691923839428460567  # Replace with your channel ID (integer)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    schedule_daily_reminder()
    await bot.tree.sync()  # Sync slash commands

def schedule_daily_reminder():
    scheduler.add_job(send_reminder, 'cron', hour=12, minute=0)  # Set time for the reminder
    scheduler.start()

async def send_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        role = discord.utils.get(channel.guild.roles, name="馬娘")  # Fetch the role by name
        await channel.send(f'{role.mention} 請訪問 [每日簽到 領取遊戲獎勵](https://uma.komoejoy.com/event/dailygift/) 以參加活動並獲得遊戲獎勵！')

@bot.tree.command(name='remind', description='Sends a reminder message mentioning the user.')
async def remind(interaction: discord.Interaction):
    """Sends a reminder message mentioning the user."""
    await interaction.response.send_message(content=f'{interaction.user.mention}, 請訪問 [每日簽到 領取遊戲獎勵](https://uma.komoejoy.com/event/dailygift/) 以參加活動並獲得遊戲獎勵！', ephemeral=True)

keep_alive()

if __name__ == "__main__":
    bot.run(TOKEN)