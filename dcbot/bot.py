import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import os

# Set your bot token and channel ID
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Replace with your bot token from .env
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
    #scheduler.add_job(send_reminder, 'interval', minutes=1)
    scheduler.add_job(send_reminder, 'cron', hour=12, minute=0)  # Set time for the reminder
    scheduler.start()

class SignInButton(View):
    def __init__(self, message):
        super().__init__()
        self.original_message = message  # Store the original message

    @discord.ui.button(label='✅ 已經簽到', style=discord.ButtonStyle.success)
    async def sign_in_button_callback(self, button: Button, interaction: discord.Interaction):
        await self.original_message.delete()  # Delete the reminder message

async def send_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        role = discord.utils.get(channel.guild.roles, name="馬娘")
        if role:
            view = SignInButton(None)  # Create an instance of the button view
            message = await channel.send(f'{role.mention} 請訪問 [每日簽到 領取遊戲獎勵](https://uma.komoejoy.com/event/dailygift/) 以參加活動並獲得遊戲獎勵！', view=view)
            view.original_message = message
        else:
            print("Role '馬娘' not found.")
    else:
        print("Channel not found.")
        
@bot.tree.command(name='remind', description='Sends a reminder message mentioning the user.')
async def remind(interaction: discord.Interaction):
    """Sends a reminder message mentioning the user."""
    await interaction.response.send_message(content=f'{interaction.user.mention}, 請訪問 [每日簽到 領取遊戲獎勵](https://uma.komoejoy.com/event/dailygift/) 以參加活動並獲得遊戲獎勵！', ephemeral=True)


if __name__ == "__main__":
    bot.run(TOKEN)