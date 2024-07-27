import subprocess
import sys
from pyrogram import Client, filters
import json

try:
    import simpleeval
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "simpleeval"])
    import simpleeval

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"🧮{prefix_userbot}math"
ccomand = " решает математические задачи"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("math", prefixes=prefix_userbot))
    def math_command(client, message):
        try:
            expression = message.text.split(maxsplit=1)[1]
            result = simpleeval.simple_eval(expression)
            message.edit(f"Результат: {result}")
        except IndexError:
            message.edit("Пожалуйста, введите математическое выражение после команды .math")
        except Exception as e:
            message.edit(f"Ошибка при вычислении выражения: {e}")
