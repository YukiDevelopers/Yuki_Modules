from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"☀{prefix_userbot}userinfo"
ccomand = " показывает информацию о пользователе"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("userinfo", prefixes=prefix_userbot))
    async def userinfo(_, message):
        if not message.reply_to_message:
            await message.reply_text("**❌Пожалуйста, ответьте на сообщение пользователя командой `.userinfo`**")
            return
        
        user = message.reply_to_message.from_user
        first_name = user.first_name if user.first_name else "Не указано"
        last_name = user.last_name if user.last_name else "Не указано"
        username = f"@{user.username}" if user.username else "Не указано"
        user_id = user.id

        reply_text = (f"**👤Информация о пользователе:**\n"
                      f"**Имя:** {first_name}\n"
                      f"**Фамилия:** {last_name}\n"
                      f"**Юзернейм:** {username}\n"
                      f"**ID:** {user_id}")
        
        await message.delete()
        await message.reply_text(reply_text)
