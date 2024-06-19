import os
import discord
from discord.ext import commands
from io import BytesIO
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())
bot.tree.copy_global_to(guild=discord.Object(id=1246014711204417546))  # Replace with your guild ID

@bot.event
async def on_ready():
    print('Connected!')
    await bot.tree.sync()  # Sync the slash commands with Discord

@bot.tree.command(name='cat', description='Get a random cat image!')
async def cat(interaction: discord.Interaction):
    try:
        url = "https://api.thecatapi.com/v1/images/search"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    cat_image = (await response.json())[0]['url']
                    async with session.get(cat_image) as img_response:
                        file = discord.File(BytesIO(await img_response.read()), filename='cat.jpg')
                        await interaction.response.send_message('Here is your cute cat!', file=file)
            except aiohttp.ClientError as e:
                print(f"Error connecting to API: {e}")
                await interaction.response.send_message(f'Error: {e}')
            finally:
                await session.close()
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')

async def retry_connect():
    while True:
        try:
            await bot.start(TOKEN)  # Use bot.start instead of bot.run
            break  # If the connection is successful, break out of the loop
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(f"Error connecting to Discord: {e}")
            await asyncio.sleep(10)  # Wait for 10 seconds before retrying

# Run the async function
asyncio.run(retry_connect())
