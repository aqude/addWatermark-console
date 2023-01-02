from config import parse_yaml
from telebot import TeleBot, types
from PIL import ImageFont, Image, ImageDraw
import os
token = parse_yaml()

bot = TeleBot(token)
# колличество повторений
count: int = 1

# клавиатура


def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(types.InlineKeyboardButton(
        "Водяной знак", callback_data="watermark"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Привет, я бот для добавления водяного знака", reply_markup=start_keyboard())

    # bot.send_message(message.chat.id, "Для добавления водяного знака введите /watermark")
    # bot.send_message(message.chat.id, "Для изменения колличества повторений /count")

# @bot.message_handler(commands=['count'])
# def count_edit(message):
#     bot.send_message(message, "Сколько раз?")
#     @bot.message_handler(content_types=['text'])
#     def handle_count(message):
#         count = message.text
#         return count
#         try:
#             print("Записал")
#         except Exception as e:
#             bot.reply_to(message , e)


@bot.callback_query_handler(func=lambda call: call.data == 'watermark')
def send_welcome(call):
    bot.send_message(call.message.chat.id, "Пришлите фото")
    bot.register_next_step_handler(call.message, get_docs_photo)
    # @bot.message_handler(content_types=['photo'])


def get_docs_photo(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id   
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("./img/image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        # принять водяной знак
        msg = bot.send_message(message.chat.id, "Введите водяной знак")
        # @bot.message_handler(content_types=['text'])
        bot.register_next_step_handler(msg, docs_photo_edit)
    else:
        msg = bot.send_message(message.chat.id, "Пришлите фото")
        bot.register_next_step_handler(msg, get_docs_photo)


def docs_photo_edit(message):
    text = message.text
    im = Image.open("./img/image.jpg")
    # размеры фото
    width, height = im.size
    heightFix = height - 100
    widthFix = width / 5
    font = ImageFont.truetype("arial.ttf", 50)
    draw = ImageDraw.Draw(im)
    # indent = 0
    # for i in range(handle_count()):
    for i in range(count):
        draw.text((widthFix, heightFix), text,
                  (255, 255, 255), font=font)
        # indent += 40
    im.save("./img/image.jpg")
    bot.send_photo(message.chat.id, open("./img/image.jpg", 'rb'))
    # удалить файл
    os.remove("./img/image.jpg")


bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()
bot.infinity_polling()
