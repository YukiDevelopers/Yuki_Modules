import subprocess
import sys


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import requests
except ImportError:
    install_package("requests")
    import requests

try:
    from mtranslate import translate
except ImportError:
    install_package("mtranslate")
    from mtranslate import translate

from pyrogram import Client, filters
from pyrogram.types import Message
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"☀{prefix_userbot}recipe"
ccomand = f"Отправляет случайный рецепт, пример: {prefix_userbot}recipe."


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("recipe", prefixes=prefix_userbot))
    async def send_random_recipe(client: Client, message: Message):
        url = "https://www.themealdb.com/api/json/v1/1/random.php"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            meal = data['meals'][0]

            recipe_title = meal['strMeal']
            recipe_instructions = meal['strInstructions']
            recipe_title_tr = translate(recipe_title, 'ru')
            recipe_instructions_tr = translate(recipe_instructions, 'ru')

            txt = f"**{recipe_title_tr}**\n\nРецепт: {recipe_instructions_tr}"
            await message.edit_text(txt, disable_web_page_preview=True)
        else:
            await message.edit_text("Ошибка при получении рецепта")
