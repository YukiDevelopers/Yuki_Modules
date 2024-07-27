from pyrogram import Client, filters
import asyncio
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"📝`{prefix_userbot}spam`"
ccomand = f" отправляет сообщение указанное количество раз с заданным интервалом. Пример: `{prefix_userbot}spam 10 привет 0.1`"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("spam", prefixes=prefix_userbot))
    async def spam(_, message):
        try:
            parts = message.text.split(" ", maxsplit=3)
            count = int(parts[1])
            text = parts[2]
            delay = float(parts[3])

            for _ in range(count):
                await message.reply_text(text)
                await asyncio.sleep(delay)

        except IndexError:
            await message.reply_text("**❌ Неправильный формат команды. Пример: `.spam 10 привет 0.1`**")
        except ValueError:
            await message.reply_text("**❌ Убедитесь, что количество сообщений и задержка указаны правильно.**")
        except Exception as e:
            await message.reply_text(f"**❌ Произошла ошибка: {e}**")
