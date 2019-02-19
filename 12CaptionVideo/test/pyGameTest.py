#coding=utf-8
# import pygame
#
# screen = pygame.display.set_mode((600,800))
# pygame.init()
#
#
# def drawText(text,posx,posy,textHeight=48,fontColor=(255,0,0),backgroudColor=(255,255,255)):
#         fontObj = pygame.font.Font('./font/test.ttf', textHeight)  # 通过字体文件获得字体对象
#         textSurfaceObj = fontObj.render(text, True,fontColor,backgroudColor)  # 配置要显示的文字
#         textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
#         textRectObj.center = (posx, posy)  # 设置显示对象的坐标
#         screen.blit(textSurfaceObj, textRectObj)  # 绘制字
#         pygame.image.save(screen,'test.png')
# drawText('hello',10,10)


import pygame
import time

pygame.init()

white = (255,255,255)

car_width = 100

display_width = 800
display_height = 600


gameDisplay = pygame.display.set_mode( (display_width,display_height) )
# pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

# carImg = pygame.image.load('car.png')

# def car(x, y):
#     gameDisplay.blit(carImg, (x,y))


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_diaplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))

    pygame.transform.rotate(TextSurf,45)

    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


    pygame.image.save(gameDisplay,'test.png')
    time.sleep(2)
    # game_loop()

def crash():
    message_diaplay('You Crashed')


def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8
    x_change = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            print(event)
        x += x_change
        gameDisplay.fill(white)
        # car(x,y)
        if x > display_width - car_width or x < 0:
            gameExit = True
        pygame.display.update()
        clock.tick(60)
crash()
#game_loop()
pygame.quit()