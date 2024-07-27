import requests
from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"📞`{prefix_userbot}phone`"
ccomand = " Ищет информацию о номере телефона."

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("phone", prefixes=prefix_userbot))
    def phone_command(_, message):
        query = message.text.split(' ', 1)[1]
        url = f"https://htmlweb.ru/geo/api.php?json&telcod={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['limit'] == 0:
                message.edit_text("❌Номер не найден")
            else:
                country = data.get('country', {})
                region = data.get('region', {})
                other = data.get('0', {})

                message.edit_text(f"**📞Нашёл информацию о номере:**\n\n"
                                  f"Страна: {country.get('name', 'Не найдено')}, {country.get('fullname', 'Не найдено')}\n"
                                  f"Город: {other.get('name', 'Не найдено')}\n"
                                  f"Почтовый индекс: {other.get('post', 'Не найдено')}\n"
                                  f"Код валюты: {country.get('iso', 'Не найдено')}\n"
                                  f"Телефонные коды: {data.get('capital', {}).get('telcod', 'Не найдено')}\n"
                                  f"Посмотреть в wiki: {other.get('wiki', 'Не найдено')}\n"
                                  f"Гос. номер региона авто: {region.get('autocod', 'Не найдено')}\n"
                                  f"Оператор: {other.get('oper', 'Не найдено')}, {other.get('oper_brand', 'Не найдено')}, {other.get('def', 'Не найдено')}\n"
                                  f"Местоположение: {country.get('name', 'Не найдено')}, {region.get('name', 'Не найдено')}, {other.get('name', 'Не найдено')} ({region.get('okrug', 'Не найдено')})\n"
                                  f"Открыть на карте (google): https://www.google.com/maps/place/{other.get('latitude', 'Не найдено')}+{other.get('longitude', 'Не найдено')}\n"
                                  f"Локация: {data.get('location', 'Не найдено')}\n"
                                  f"Язык общения: {country.get('lang', 'Не найдено').title()}, {country.get('langcod', 'Не найдено')}\n"
                                  f"Столица: {data.get('capital', {}).get('name', 'Не найдено')}\n"
                                  f"Широта/Долгота: {other.get('latitude', 'Не найдено')}, {other.get('longitude', 'Не найдено')}\n"
                                  f"Оценка номера в сети: https://phoneradar.ru/phone/{query}")
        else:
            message.edit_text("❌Ошибка при запросе к API.")

print("Модуль phone загружен!")
