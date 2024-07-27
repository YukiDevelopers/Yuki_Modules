import requests
from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"📞`{prefix_userbot}ip`"
ccomand = " Ищет информацию о IP-адресе."


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("ip", prefixes=prefix_userbot))
    def ip_command(_, message):
        query = message.text.split(' ', 1)[1]
        url = f"https://ipapi.co/{query}/json/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            message.edit_text(f"**📊Нашёл информацию о IP-адресе:**\n\n"
                              f"IP: {data.get('ip', 'Не найдено')}\n"
                              f"Версия IP: {data.get('version', 'Не найдено')}\n"
                              f"Страна: {data.get('country_name', 'Не найдено')} ({data.get('country_code_iso3', 'Не найдено')})\n"
                              f"Регион: {data.get('region', 'Не найдено')}\n"
                              f"Город: {data.get('city', 'Не найдено')}\n"
                              f"Почтовый индекс: {data.get('postal', 'Не найдено')}\n"
                              f"Широта: {data.get('latitude', 'Не найдено')}\n"
                              f"Долгота: {data.get('longitude', 'Не найдено')}\n"
                              f"ASN: {data.get('asn', 'Не найдено')}\n"
                              f"Организация: {data.get('org', 'Не найдено')}\n"
                              f"Провайдер: {data.get('provider', 'Не найдено')}\n"
                              f"Тип IP: {data.get('type', 'Не найдено')}")
        else:
            message.edit_text("❌Ошибка при запросе к API.")

print("Модуль ip загружен!")
