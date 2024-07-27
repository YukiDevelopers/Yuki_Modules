from pyrogram import Client, filters
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"🔄`{prefix_userbot}swap`"
ccomand = " Изменяет раскладку текста. автор: (`@im_del_acc`)"


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("swap", prefixes=prefix_userbot))
    def swap(_, message):
        # Проверяем, есть ли сообщение для ответа
        if message.reply_to_message:
            original_text = message.reply_to_message.text
            if original_text:
                swapped_text = swap_layout(original_text)
                message.reply_to_message.reply_text(swapped_text)
                message.delete()
            else:
                message.edit("❗️ Ошибка: Нет текста для изменения.")
        else:
            message.edit("❗️ Ответьте на сообщение которое нужно свапнуть!")

eng_to_rus = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~`!@#$%^&*()_+",
    "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ёё!\"№;%:?*()_+"
)
rus_to_eng = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ёё!\"№;%:?*()_+",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~`!@#$%^&*()_+"
)


def swap_layout(text):
    words = text.split()
    swapped_words = []
    for word in words:
        if word.isupper():
            swapped_word = word.lower().translate(
                rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus)
            swapped_words.append(swapped_word.upper())
        else:
            swapped_words.append(
                word.translate(rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus))
    return ' '.join(swapped_words)
