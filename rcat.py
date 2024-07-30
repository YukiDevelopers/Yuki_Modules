import json
from PIL import Image
import requests
from pyrogram import Client, filters
import io

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"☀{prefix_userbot}rcat"
ccomand = f"🐈 Ищет рендомную картинку кота"


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("rcat", prefixes=prefix_userbot))
    async def send_cat_image(client, message):
        url = "https://api.thecatapi.com/v1/images/search"
        response = requests.get(url)

        if response.status_code == 200:
            img_url = response.json()[0]['url']
            response = requests.get(img_url)
            img = Image.open(io.BytesIO(response.content))

            if img.mode == 'P':
                img = img.convert('RGB')

            output = io.BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, photo=output)
