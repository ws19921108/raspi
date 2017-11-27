import pygame, sys, os
import pygame.camera
from pygame.locals import *
import tkinter.filedialog

pygame.init()
# pygame.camera.init()
# camera = pygame.camera.Camera('/dev/video0')
# camera.start()

win_width = 800
win_height = 600
img_width = 640
img_height = 480
border = 5

screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('BBbird中文版')

font = pygame.font.Font("simhei.ttf", 32)

sub_lefttop = screen.subsurface((0,0,img_width,img_height))
sub_leftbottom  = screen.subsurface((0,img_height,img_width,win_height-img_height))
sub_right  = screen.subsurface((img_width,0,win_width-img_width,win_height))
rect_lefttop = sub_lefttop.get_rect().move(sub_lefttop.get_offset())
rect_leftbottom = sub_leftbottom.get_rect().move(sub_leftbottom.get_offset())
rect_right = sub_right.get_rect().move(sub_right.get_offset())


img = pygame.image.load(os.path.join('img', '123.png'))
img = pygame.transform.scale(img, (img_width, img_height))
pygame.draw.rect(sub_lefttop, Color(255, 0, 255), sub_lefttop.get_rect(), border)
sub_lefttop.blit(img, (0, 0))

cb_text = font.render('a--添加\to--验证\tl--LED开关\tq--退出', 1, Color(200, 200, 200))
pygame.draw.rect(sub_leftbottom, Color(255, 255, 0), sub_leftbottom.get_rect(), border)
sub_leftbottom.blit(cb_text, (10,10))


led_rect = Rect(55,20,50,50)
led_color = Color(100, 100, 100)
lock_rect = Rect(55,150,50,50)
lock_color = Color(100, 100, 100)
led_text = font.render("灯", 1, Color(255, 0, 0))
lock_text = font.render("锁", 1, Color(255, 0, 0))
pygame.draw.ellipse(sub_right, led_color, led_rect)
pygame.draw.ellipse(sub_right, lock_color, lock_rect)
pygame.draw.rect(sub_right, Color(0, 255, 255), sub_right.get_rect(), border)
sub_right.blit(led_text, (60,75))
sub_right.blit(lock_text, (60,205))

bg_color = Color(0, 0, 0)
led_on = False
response = ''
pygame.display.update()
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == ord('l'):
                led_on = not led_on
                if led_on:
                    led_color = Color(255, 255, 255)
                    response = '开灯'
                else:
                    led_color = Color(100, 100, 100)
                    response = '关灯'
                pygame.draw.ellipse(sub_right, led_color, led_rect)
                pygame.display.update(rect_right)
            elif event.key == ord('a'):
                response = '添加照片'
                # img = camera.get_image()
                filename = tkinter.filedialog.asksaveasfilename(filetypes=[("jpg格式", ".jpg")])
                if filename != '':
                    if filename[-4:] != '.jpg':
                        filename += '.jpg'
                    pygame.image.save(img,filename.encode('gb2312'))
            elif event.key == ord('o'):
                response = '人脸识别'
            elif event.key == ord('q'):
                # camera.stop()
                pygame.quit()
                sys.exit()
            res_text = font.render(response, 1, Color(200, 200, 200))
            sub_leftbottom.fill(bg_color, Rect(10,60,620,50))
            sub_leftbottom.blit(res_text, (300, 60))
            pygame.display.update(rect_leftbottom)
        elif event.type == QUIT:
            # camera.stop()
            pygame.quit()
            sys.exit()
    # image = camera.get_image()
    # sub_lefttop.blit(image, (0, 0))
    pygame.display.update(rect_lefttop)




