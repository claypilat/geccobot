import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
intents = discord.Intents.default()
intents.message_content = True
import json
from discord.ext import commands, tasks
import time
import asyncio

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)
discord_token = ""

@client.event
async def on_ready():
    # Find the channel where you want the bot to send a message
    channel = client.get_channel(1084710357337124996)  # Replace with your channel ID
    my_background_task.start()
    # Send a message to the channel
    await channel.send("`Geccobot is booting...`")
    #await my_background_task()


last_transaction_hash = []

@client.event
async def on_message(message):
    if message.content.startswith('!gecid'):
        # Define paths to images and font
        
        template_path = "C:/Users/clayt/Desktop/geccobot/template.png"
        layer1_path = "C:/Users/clayt/Desktop/geccobot/layer1.png"
        layer2_path = "C:/Users/clayt/Desktop/geccobot/layer2.png"
        font_path = "C:\\Users\\clayt\\AppData\\Local\\Microsoft\\Windows\\Fonts\\AKZIDENZGROTESKPRO_BOLDEX.OTF"

        # Open images
        original_image = Image.open(template_path)
        profile_image_bytes = await message.author.avatar.read()
        replacement_image = Image.open(BytesIO(profile_image_bytes)).resize((270, 335))
        layer1 = Image.open(layer1_path)
        layer2 = Image.open(layer2_path)

        # Create mask for rounded corners
        mask = Image.new("L", replacement_image.size, 0)
        draw = ImageDraw.Draw(mask)
        radius = 15
        draw.pieslice((0, 0, radius*2, radius*2), 180, 270, fill=255)
        draw.pieslice((0, replacement_image.height - radius*2, radius*2, replacement_image.height), 90, 180, fill=255)
        draw.pieslice((replacement_image.width - radius*2, 0, replacement_image.width, radius*2), 270, 360, fill=255)
        draw.pieslice((replacement_image.width - radius*2, replacement_image.height - radius*2, replacement_image.width, replacement_image.height), 0, 90, fill=255)
        draw.rectangle((0, radius, replacement_image.width, replacement_image.height - radius), fill=255)
        draw.rectangle((radius, 0, replacement_image.width - radius, replacement_image.height), fill=255)
        replacement_image.putalpha(mask)

        # Blend images
        blend1 = Image.blend(layer1, replacement_image, 0.98)
        blend2 = Image.blend(layer2, blend1, 0.98)

        # Paste blended image onto original image
        original_image.paste(blend2, (275, 372), blend2)

        # Add text to the final image
        draw = ImageDraw.Draw(original_image)
        text = f"{message.author.name}#{message.author.discriminator}"
        text = text.upper()
        font = ImageFont.truetype(font_path, 36)
        draw.text((750, 415), text, fill=(24, 51, 78), font=font)

        # Save the modified image to a buffer
        modified_image_buffer = BytesIO()
        original_image.save(modified_image_buffer, format='PNG')
        modified_image_buffer.seek(0)

        # Send the modified image as a message attachment
        await message.channel.send(file=discord.File(modified_image_buffer, filename='modified_image.png'))


@tasks.loop(seconds = 25)
async def my_background_task():
        channel = client.get_channel(1085615827522424863)  # Replace with your channel ID
        #await channel.send("`Looking on chain....`")
        global last_transaction_hash
        #while True:
        url = "https://eth-mainnet.g.alchemy.com/nft/v2/ALCH CODE/getNFTSales?fromBlock=0&toBlock=latest&order=desc&contractAddress=0xb97ca772f6e5d9a68b24c68e3be77990fa7abfb9&limit=10"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        data = json.loads(response.text)

        if 'nftSales' in data:
            nft_sales = data['nftSales']
        else:
            print("Error: 'nftSales' key not found in the response.")

        for sale in nft_sales:
            eth_price = float(sale['sellerFee']['amount']) / (10 ** sale['sellerFee']['decimals'])
            transaction_hash = sale['transactionHash']
            token_id = sale['tokenId']
            print(f"ETH Amount {eth_price:.2f}")
            print(f"Token {token_id}")
            print(f"Transaction Hash: {transaction_hash}")

            if transaction_hash not in last_transaction_hash:
                last_transaction_hash.append(transaction_hash)
                url = f"https://eth-mainnet.g.alchemy.com/nft/v2/ALCH CODE/getNFTMetadata?contractAddress=0xb97ca772f6e5d9a68b24c68e3be77990fa7abfb9&tokenId={token_id}&refreshCache=false"

                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)

                image_url = data["metadata"]["image"]

                # Create an embed
                embed = discord.Embed(title=f"`GANZ {token_id} JUST SOLD FOR {eth_price:.2f} !`", description=image_url, color=0x00ff00)
                embed.set_image(url=image_url)

                await channel.send(embed=embed)
 

# Replace 'TOKEN' with your bot token
client.run(discord_token)
