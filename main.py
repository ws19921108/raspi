import pygame, sys, os
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('BBbird')
img = pygame.image.load(os.path.join('img', '123.png'))
img = pygame.transform.scale(img, (400, 300))
font = pygame.font.SysFont("arial", 36)
led_text = font.render('LED', 1, Color(255, 0, 0))
screen.blit(led_text, (450,100))
screen.blit(img, (0, 0))
led_rect = Rect(450,50,50,50)
led_color = Color(100, 100, 100)
pygame.draw.ellipse(screen, led_color, led_rect)
led_on = False
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == ord('l'):
                led_on = not led_on
                if led_on:
                    led_color = Color(255, 255, 255)
                else:
                    led_color = Color(100, 100, 100)
                pygame.draw.ellipse(screen, led_color, led_rect)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()