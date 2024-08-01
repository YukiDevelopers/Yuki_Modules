import datetime
import json
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"{prefix_userbot}sft"
ccomand = "Сфт"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("sft", prefixes=prefix_userbot))
    async def sft(_, message):
        if len(message.command) != 2:
            await message.edit("**Использование: sft <имя_файла>.<расширение>**")
            return

        if not message.reply_to_message:
            await message.edit("**Пожалуйста, сделайте реплай на сообщение с кодом.**")
            return

        file_name = message.command[1]
        code = message.reply_to_message.text

        with open(file_name, "w") as file:
            file.write(code)
            await message.delete()

        await message.reply_document(file_name, caption="Создатель модуля: @umvdoxxxy")
