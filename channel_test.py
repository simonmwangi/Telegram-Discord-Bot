import discord
import configparser
import os
from discord.ext import commands

config_path = os.path.join('credentials.ini')
#os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Creates a configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Set up your Telegram API credentials
TOKEN = config['Credentials']['discord_bot_token']

# Initialize the bot client
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
    #channel = client.get_channel('')

@bot.command()
async def send_message(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        await ctx.send(f'Channel with ID {channel_id} not found.')

# Run the bot
bot.run(TOKEN)
