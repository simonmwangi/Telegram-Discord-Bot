import os
import time
import configparser
import telethon
from telethon import TelegramClient, sync, events
import discord
from discord.ext import commands

config_path = os.path.join('credentials.ini')
#os.makedirs(os.path.dirname(config_path), exist_ok=True)

# Creates a configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Set up your Telegram API credentials
api_id = config['Credentials']['telegram_api_id']
api_hash = config['Credentials']['telegram_api_hash']
phone_number = config['Credentials']['telegram_phone_no']

discord_bot_token = config['Credentials']['discord_bot_token']

# Create a Discord bot
intents = discord.Intents.default()
discord_bot = commands.Bot(command_prefix='!', intents=intents)

# List of channels to monitor
channels_to_monitor = list(config['Channels']['channels_to_monitor'].split(','))#.split()  # 'channel2', 'channel3']
print(channels_to_monitor)

# Create a Telegram client
client = TelegramClient(phone_number, api_id, api_hash)


# Function to forward messages and pictures to your saved messages
async def forward_to_discord_channel(event):
    discord_channel = discord_bot.get_channel(int(config['Channels']['discord_channel_id']))
    print(discord_channel)
    print(type(config['Channels']['discord_channel_id']))

    # Get the saved message chat entity
    #saved_messages = await client.get_entity('me')

    if isinstance(event.message.media, telethon.types.MessageMediaPhoto):
        #await client.forward_messages(saved_messages, event.message)
        file = await event.message.download_media()
        await discord_channel.send(file=discord.File(file))
    elif isinstance(event.message.media, telethon.types.MessageMediaDocument):
        #await client.forward_messages(saved_messages, event.message)
        file = await event.message.download_media()
        await discord_channel.send(file=discord.File(file))
    elif event.message.text:
        #await client.forward_messages(saved_messages, event.message)
        await discord_channel.send(event.message.text)


# Start the client and listen for new messages
async def main():
    async with client:
        for channel in channels_to_monitor:
            @client.on(events.NewMessage(chats=channel))
            async def handler(event):
                await forward_to_discord_channel(event)
                
        await discord_bot.start(discord_bot_token)
        await client.run_until_disconnected()


if __name__ == '__main__':
    client.start()
    #discord_bot.loop.run_until_complete(main())
    client.loop.run_until_complete(main())
