import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

    
@client.event
async def on_ready():
    # Find the channel where you want the bot to send a message
    channel = client.get_channel(1084710357337124996)  # Replace with your channel ID
    
    # Send a message to the channel
    await channel.send("Hello World!")


import discord
from PIL import Image, ImageDraw, ImageFont
import io


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



# Replace 'TOKEN' with your bot token
client.run('INSERT CODE')
