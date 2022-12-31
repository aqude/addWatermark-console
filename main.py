from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import click
@click.command()
@click.option('--filew', help='add file.')
@click.option('--text', prompt='add watermark "1-2" or write "text"',
              help='The person to greet.')

# https://habr.com/ru/post/592089/
def photoRead(filew: str, text: str):
    im = Image.open(filew)

    if text == "1":
        text = Image.open('watermark1.png')
        im.paste(text, (0, 0))
        im.show()
    elif text == "2":
        text = Image.open('watermark2.png')
        im.paste(text, (0, 0))
        im.show()
    elif text == "text":
        textWaterMark = click.prompt('add watermark text', type=str)
        count = click.prompt('number of repetitions', type=int, default=1)
        font = ImageFont.truetype("arial.ttf", 50)
        draw = ImageDraw.Draw(im)
        indent = 0
        for i in range(count):
            draw.text((0, indent), textWaterMark,(255,255,255),font=font)
            indent += 40
        im.show()
    

if __name__ == '__main__':
    photoRead()