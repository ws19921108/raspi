#coding:utf-8
import pygame, sys, os
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('BBbird中文版')
img = pygame.image.load(os.path.join('img', '123.png'))
img = pygame.transform.scale(img, (400, 300))
font = pygame.font.SysFont("microsoftyahei", 36)
led_text = font.render("灯", 1, Color(255, 0, 0))
cb_text = font.render('what can i help you?', 1, Color(200, 200, 200))

bg_color = Color(0, 0, 0)
led_rect = Rect(450,50,50,50)
led_color = Color(100, 100, 100)
pygame.draw.ellipse(screen, led_color, led_rect)
pygame.draw.rect(screen, Color(255, 0, 255), (0,0,400,300), 5)
pygame.draw.rect(screen, Color(255, 255, 0), (0,300,400,300), 5)
pygame.draw.rect(screen, Color(0, 255, 255), (400,0,400,600), 5)
led_on = False

screen.blit(cb_text, (10,300))

screen.blit(led_text, (450,100))
screen.blit(img, (0, 0))

text = ''
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == 308:
                led_on = not led_on
                if led_on:
                    led_color = Color(255, 255, 255)
                else:
                    led_color = Color(100, 100, 100)
                pygame.draw.ellipse(screen, led_color, led_rect)

                cb_text.fill(bg_color)
                screen.blit(cb_text, (10, 300))
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()