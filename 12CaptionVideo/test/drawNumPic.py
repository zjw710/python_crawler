# -*- coding:utf-8 -*-

from PIL import Image,ImageFont,ImageDraw,ImageFilter
import random
import os
import time

imgWidth = 20
imgHeight = 24
fontSize = 28
backGroundColor = (255,)*4
fontColor = (0,)*3
text = 'H'

font = ImageFont.truetype('./font/test.ttf', fontSize)

codeimg = Image.new('RGBA',(imgWidth,imgHeight), backGroundColor)

imagePath = './codes'
if not os.path.exists(imagePath):
    os.mkdir(imagePath)

textWidth, textHeight = font.getsize(text)
textLeft = (imgWidth-textWidth)/2
textTop = (imgHeight-textHeight)/2

draw = ImageDraw.Draw(codeimg)
draw.text(xy=(textLeft,textTop),text=text,fill=fontColor,font=font)

rot = codeimg.rotate(45,expand=0)
# codeimg.rotate
fff = Image.new('RGBA', rot.size,backGroundColor)
codeimg = Image.composite(rot, fff, rot)
codeimg.show()

# codeimg.save('./codes/test.jpg')