from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import json
import os

AFK_FILE = "afk_status.json"
CONFIG_FILE = "config.json"

afk_status = {}

if os.path.exists(AFK_FILE):
    with open(AFK_FILE, "r") as file:
        afk_status = json.load(file)

def save_afk_status():
    with open(AFK_FILE, "w") as file:
        json.dump(afk_status, file, ensure_ascii=False, indent=4)

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"☀{prefix_userbot}afk"
ccomand = f" включает и выключает режим AFK.\nПример: {prefix_userbot}afk <причина>\nПример: {prefix_userbot}afkoff"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("afk", prefixes=prefix_userbot))
    async def set_afk_mode(client: Client, message: Message):
        chat_id = str(message.chat.id)
        afk_status[chat_id] = {
            "afk_mode": True,
            "afk_reason": " ".join(message.command[1:]),
            "afk_start_time": datetime.now().isoformat()
        }
        save_afk_status()
        await message.edit_text("😴 AFK включено!")

    @app.on_message(filters.me & filters.command("afkoff", prefixes=prefix_userbot))
    async def unset_afk_mode(client: Client, message: Message):
        chat_id = str(message.chat.id)
        if chat_id in afk_status:
            afk_status[chat_id]["afk_mode"] = False
            save_afk_status()
            await message.edit_text("🥱 AFK выключено!")

    @app.on_message(filters.mentioned)
    async def check_afk(client: Client, message: Message):
        chat_id = str(message.chat.id)
        if chat_id in afk_status and afk_status[chat_id]["afk_mode"]:
            afk_start_time = datetime.fromisoformat(afk_status[chat_id]["afk_start_time"])
            current_time = datetime.now()
            time_diff = current_time - afk_start_time
            await message.reply_text(f"💤 Юзер сейчас в AFK.\nВремя AFK - {time_diff}\nПричина - {afk_status[chat_id]['afk_reason']}\n\nСоздатель модуля: (`@im_del_acc`)")

    @app.on_message(filters.me & filters.command("afk help", prefixes=prefix_userbot))
    async def afk_help(client: Client, message: Message):
        help_text = (f"**ℹ️ Помощь по модулю AFK:**\n\n"
                     f"**{prefix_userbot}afk <причина>** - Включает режим AFK с указанной причиной.\n"
                     f"**{prefix_userbot}afkoff** - Выключает режим AFK.\n"
                     f"**{prefix_userbot}afk help** - Показать эту помощь.\n\n"
                     f"**Пример использования:**\n"
                     f"Включение AFK: `{prefix_userbot}afk Ухожу на обед`\n"
                     f"Выключение AFK: `{prefix_userbot}afkoff`\n\n(`@im_del_acc`)")
        await message.reply_text(help_text)

