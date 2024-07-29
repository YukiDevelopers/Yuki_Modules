import asyncio
import random
import aiohttp
import os
from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"
DATABASE_URL = "https://github.com/YukiDevelopers/Yuki_Modules/raw/main/mqone_database.txt"
DATABASE_FILE = "mqone_database.txt"
TASK_RUNNING = False

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']


cinfo = f"☀{prefix_userbot}mq"
ccomand = f"Уничтожить пидора"


async def download_database():
    async with aiohttp.ClientSession() as session:
        async with session.get(DATABASE_URL) as response:
            if response.status == 200:
                content = await response.text()
                with open(DATABASE_FILE, "w") as file:
                    file.write(content)
                return True
            else:
                return False


async def send_random_message(client, chat_id, delay):
    global TASK_RUNNING
    TASK_RUNNING = True
    with open(DATABASE_FILE, "r") as file:
        lines = file.readlines()

    while TASK_RUNNING:
        message = random.choice(lines).strip()
        await client.send_message(chat_id, message)
        await asyncio.sleep(delay)


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("mq", prefixes=prefix_userbot))
    async def handle_mq_command(client, message):
        global TASK_RUNNING
        chat_id = message.chat.id
        command = message.command

        if len(command) == 1:
            if TASK_RUNNING:
                TASK_RUNNING = False
                await message.reply("**слит петушара ебанная**")
            else:
                await message.edit("**дурень укажи таймнг в секундах после команды.**")
            return

        if len(command) != 2:
            await message.edit("дурень укажи таймнг в секундах после команды")
            return

        try:
            delay = int(command[1])
        except ValueError:
            await message.edit("Еблан? тайминг должен быть числом")
            return

        if not os.path.exists(DATABASE_FILE):
            await message.edit("Сек базу данных загружаю...")
            success = await download_database()
            if not success:
                await message.delete()
                await client.send_message(chat_id, "не получилось базу данных загрузить, проверь инет.")
                return
            await message.delete()
            await client.send_message(chat_id, "База загружена, развлекайся!")

        if TASK_RUNNING:
            TASK_RUNNING = False
            await message.delete()
            await message.send_message("**слит петушара ебанная**")
        else:
            await message.edit(f"`я` **тебя уничтожу сука**")
            asyncio.create_task(send_random_message(client, chat_id, delay))
