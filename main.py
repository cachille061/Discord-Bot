from typing import Final # Have to make sure typing module is installed first. (Can do python -m pip install typing in terminal. pip is python package manager -m is module)
# This line imports the FINAL constant from the typing module. FINAL is a constant used as a type hint to indicate that a variable should not be reassigned. 
# It's typically used in variable annotations to denote that a variable is intended to be a constant and should not be modified after its initial assignment. 
import os 
# This line imports the os module, which provides a way to interact with the operating system. The os module contains various functions for operating system-dependent functionality such as file operations, environment variables, and process management. 
# By importing os, you gain access to these functionalities, allowing you to perform tasks like file manipulation, directory operations, and more in your Python code.
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import requests
import asyncio # Import asyncio module for sleep function

import fortnite_api

# Load environment variables
load_dotenv()

# Fetch api_key from environment variables
api_key = os.getenv('api_key')

# STEP 1: LOAD OUR TOKEN FROM SOMEWHERE SAFE
TOKEN = os.getenv('DISCORD_TOKEN')

# STEP 2: BOT SETUP
intents = Intents.default()
intents.message_content = True 
client = Client(intents=intents)

# Initialize Fortnite API
api = fortnite_api.FortniteAPI(api_key=api_key, run_async=True)

# STEP 3: DEFINE COMMAND TO GET FORTNITE SHOP ITEMS
import logging

# Initialize logger
logger = logging.getLogger(__name__)

async def get_fortnite_shop():
    try:
        # Fetch the shop data
        shop_data = await api.shop.fetch()
 
        # Check if the shop data is available
        if shop_data is None:
            logger.error("Failed to fetch Fortnite shop data. Shop data is None.")
            return "Failed to fetch Fortnite shop data. Please try again later."
        
        if shop_data.daily is None:
            logger.error("Failed to fetch Fortnite shop data. Shop data.daily is None.")

        # Initialize an empty string to store the shop message
        shop_message = "Daily Shop Items:\n\n"

        # Iterate over the daily shop entries
        for entry in shop_data.daily.entries:
            shop_message += f"Name: {entry.dev_name}\n"
            shop_message += f"Regular Price: {entry.regular_price}\n"
            shop_message += f"Final Price: {entry.final_price}\n"
            shop_message += f"Giftable: {'Yes' if entry.giftable else 'No'}\n"
            shop_message += f"Refundable: {'Yes' if entry.refundable else 'No'}\n"
            shop_message += "\n"

        return shop_message
    except Exception as e:
        logger.exception("An error occurred while fetching Fortnite shop data.")
        return f"An error occurred: {str(e)}"

# STEP 4: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 5: HANDLING ALL INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    if user_message.lower().strip() == "!fortnite_shop":
        try:
            response = await get_fortnite_shop()
            await message.channel.send(response)
        except Exception as e:
            print(e)
    else:
        await send_message(message, user_message)

# STEP 6: PING SERVER EVERY 20 MINUTES
async def ping_server():
    while True:
        await asyncio.sleep(1200)  # Sleep for 20 minutes (20 minutes * 60 seconds)
        guild = client.get_guild(1205928138085765120) # Server ID
        if guild:
            channel = guild.get_channel(1206099867534102538) # Channel ID
            if channel:
                await channel.send("Ping!")  # Send ping message

# STEP 7: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready()-> None:   
    print(f'{client.user} is now running!')
    asyncio.create_task(ping_server())  # Start the ping server task when bot is ready


# STEP 8: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()