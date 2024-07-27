import pyrogram
import json
from pyrogram.types import ChatPermissions
from pyrogram import Client, filters
import datetime

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"🔇`{prefix_userbot}mute`"
ccomand = " Mute/Unmute user example: {prefix_userbot}mute 500 (in seconds) or {prefix_userbot}unmute"


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("mute", prefixes=prefix_userbot))
    def mute_command(client, message):
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            args = message.text.split()
            if len(args) < 2:
                message.edit_text("❌Укажите время мута!")
                return
            try:
                time = int(args[1])
                if time < 1:
                    message.edit_text("❌Время мута должно быть больше 0!")
                    return
            except ValueError:
                message.edit_text("❌Неверный формат времени!")
                return

            try:
                until_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
                client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date
                )
                message.edit_text(f"✅Пользователь мут на {time} секунд!")
            except pyrogram.errors.Forbidden:
                message.edit_text("❌У вас нет прав на мут пользователей в этом чате!")
        else:
            message.edit_text("❌Ответьте на сообщение пользователя, которого хотите замутить!")

    @app.on_message(filters.me & filters.command("unmute", prefixes=prefix_userbot))
    def unmute_command(client, message):
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            try:
                client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_send_polls=True,
                    )
                )
                message.edit_text("✅Пользователь размучен!")
            except pyrogram.errors.Forbidden:
                message.edit_text("❌У вас нет прав на размучение пользователей в этом чате!")
        else:
            message.edit_text("❌Ответьте на сообщение пользователя, которого хотите размутить!")
