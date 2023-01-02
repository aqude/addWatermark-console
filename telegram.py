from config import parse_yaml
from telebot import TeleBot, types
from PIL import ImageFont, Image, ImageDraw
import os
token = parse_yaml()

bot = TeleBot(token)
# колличество повторений
count: int = 1
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Для добавления водяного знака введите /watermark")
    bot.reply_to(message, "Для изменения колличества повторений /count")


@bot.message_handler(commands=['count'])
def count_edit(message): 
    bot.reply_to(message, "Сколько раз?")
    @bot.message_handler(content_types=['text'])
    def handle_count(message):
        count = message.text
        return count
        try:
            print("Записал")
        except Exception as e:
            bot.reply_to(message , e)


# принять команду и потом фото
@bot.message_handler(commands=['watermark'])
def send_welcome(message):
    bot.reply_to(message, "Пришлите фото")
    @bot.message_handler(content_types=['photo'])
    def handle_docs_photo(message):
        fileID = message.photo[-1].file_id   
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("./img/image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        # принять водяной знак
        bot.reply_to(message, "Введите водяной знак")
        @bot.message_handler(content_types=['text'])
        def handle_docs_photo_edit(message):
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
                draw.text((widthFix, heightFix), text,(255,255,255),font=font)
                # indent += 40
            im.save("./img/image.jpg")
            bot.send_photo(message.chat.id, open("./img/image.jpg", 'rb'))
            # удалить файл
            os.remove("./img/image.jpg")
    pass


bot.polling()