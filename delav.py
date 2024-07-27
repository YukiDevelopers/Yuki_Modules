from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']


cinfo = f"☀{prefix_userbot}removeavatars"
ccomand = " Удаляет все аватарки."

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("removeavatars", prefixes=prefix_userbot))
    async def remove_avatars(_, message):
        try:
            profile_photos = app.get_chat_photos("me")
            
            async for photo in profile_photos:
                await app.delete_profile_photos(photo.file_id)
            
            await message.reply_text("**✅ Все аватарки удалены.**")
        except Exception as e:
            await message.reply_text(f"**❌ Произошла ошибка при удалении аватарок: {e}**")