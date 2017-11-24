#coding:utf-8
import pygame, sys, os
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()
camera = pygame.camera.Camera('/dev/video0',(400,300))
camera.start()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('BBbird中文版')

font = pygame.font.SysFont("microsoftyahei", 36)

sub_lefttop = screen.subsurface((0,0,400,300))
sub_leftbottom  = screen.subsurface((0,300,400,300))
sub_right  = screen.subsurface((400,0,400,600))
rect_lefttop = sub_lefttop.get_rect().move(sub_lefttop.get_offset())
rect_leftbottom = sub_leftbottom.get_rect().move(sub_leftbottom.get_offset())
rect_right = sub_right.get_rect().move(sub_right.get_offset())


img = pygame.image.load(os.path.join('img', '123.png'))
img = pygame.transform.scale(img, (400, 300))
pygame.draw.rect(sub_lefttop, Color(255, 0, 255), sub_lefttop.get_rect(), 5)
sub_lefttop.blit(img, (0, 0))

cb_text = font.render('what can i help you?', 1, Color(200, 200, 200))
pygame.draw.rect(sub_leftbottom, Color(255, 255, 0), sub_leftbottom.get_rect(), 5)
sub_leftbottom.blit(cb_text, (10,10))


led_rect = Rect(0,0,50,50)
led_color = Color(100, 100, 100)
led_text = font.render("灯", 1, Color(255, 0, 0))
pygame.draw.ellipse(sub_right, led_color, led_rect)
pygame.draw.rect(sub_right, Color(0, 255, 255), sub_right.get_rect(), 5)
sub_right.blit(led_text, (50,100))

bg_color = Color(0, 0, 0)
led_on = False
pygame.display.update()
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == 308:
                led_on = not led_on
                if led_on:
                    led_color = Color(255, 255, 255)
                else:
                    led_color = Color(100, 100, 100)
                pygame.draw.ellipse(sub_right, led_color, led_rect)
                pygame.display.update(rect_right)

        elif event.type == QUIT:
            pygame.quit()
            camera.stop()
            pygame.camera.quit()
            sys.exit()
    image = camera.get_image()
    sub_lefttop.blit(image, (0, 0))
    pygame.display.update(rect_lefttop)
