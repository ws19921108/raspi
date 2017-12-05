import threading, time
import pygame, sys, os
import pygame.camera
from pygame.locals import *
from aipFace import aipFace, get_file_content, aipSpeech
from time import sleep
from audio import playMp3, startRecord, stopRecord
from tuling import tuling


pygame.init()

while True:
    try:
        pygame.camera.init()
        sleep(1)
        cam_list = pygame.camera.list_cameras()
        sleep(1)
        camera = pygame.camera.Camera(cam_list[0])
        sleep(1)
        camera.start()
        break
    except:
        print('restart cam')

win_width = 800
win_height = 600
img_width = 640
img_height = 480
border = 5
font_size = 28
group = 'test'
uid = 0

screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('BBbird中文版')

font = pygame.font.Font("simhei.ttf", font_size)

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


cb_text = font.render('你：', 1, Color(200, 200, 200))
pygame.draw.rect(sub_leftbottom, Color(255, 255, 0), sub_leftbottom.get_rect(), border)
sub_leftbottom.blit(cb_text, (10,10))


led_rect = Rect(55,20,50,50)
led_color = Color(100, 100, 100)
lock_rect = Rect(55,150,50,50)
lock_color = Color(100, 100, 100)
led_text = font.render("灯", 1, Color(255, 0, 0))
lock_text = font.render("门", 1, Color(255, 0, 0))
pygame.draw.ellipse(sub_right, led_color, led_rect)
pygame.draw.ellipse(sub_right, lock_color, lock_rect)
pygame.draw.rect(sub_right, Color(0, 255, 255), sub_right.get_rect(), border)
sub_right.blit(led_text, (60,75))
sub_right.blit(lock_text, (60,205))

bg_color = Color(0, 0, 0)
led_on = False
ask = '你：'
response = ''
info = ''
enterFlag = False
pygame.display.update()
image = camera.get_image()

def video():
    #global image, sub_lefttop, rect_left_top
    while True:
        image = camera.get_image()
        sub_lefttop.blit(image, (0, 0))
        pygame.display.update(rect_lefttop)

video_thd = threading.Thread(target=video)
video_thd.setDaemon(True)
video_thd.start()

def printLine(m, text):
    line_list = [(10, 10), (10, 60)]
    sub_leftbottom.fill(bg_color, Rect(line_list[m][0], line_list[m][1], 620, 80))
    line = font.render(text, 1, Color(200, 200, 200))
    sub_leftbottom.blit(line, line_list[m])
    pygame.display.update(rect_leftbottom)

def setLED(led_on):
    color = Color(255, 255, 255) if led_on else Color(100, 100, 100)
    pygame.draw.ellipse(sub_right, color, led_rect)
    pygame.display.update(rect_right)

def unLock(lock_on):
    color = Color(255, 255, 255) if lock_on else Color(100, 100, 100)
    pygame.draw.ellipse(sub_right, color, lock_rect)
    pygame.display.update(rect_right)

def recording(flag):
    color = Color(200, 0, 0) if flag else Color(0, 0, 0)
    pygame.draw.ellipse(sub_leftbottom, color, Rect(600,10,30,30))
    pygame.display.update(rect_leftbottom)

def text2voice(text):
    result = aipSpeech.synthesis(text, 'zh', 1, {
            'vol': 5,
    })
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
    time.sleep(0.2)
    playMp3('audio.mp3')

def openTheDoor():
    pygame.image.save(image, 'tmp.jpg')
    result = aipFace.identifyUser(group, get_file_content('tmp.jpg'))
    if 'result' in result:
        item = result['result'][0]

        info = item['user_info']
        score = item['scores'][0]
        if score >= 75:
            unLock(True)
            res = '欢迎，' + info
        else:
            res = '你好，陌生人'
    else:
        res = '未获取到有效头像'
    printLine(1, res)
    text2voice(res)


words = {'开灯': setLED(True), '关灯': setLED(False), '开门': openTheDoor(), '关门': unLock(False)}

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if enterFlag == True:
                key = event.key
                if (key >= 48 and key <=57) or (key >= 97 and key <= 122):
                    info += chr(key)
                    response = info
                elif key == 13:
                    if len(info) > 0:
                        uid += 1
                        aipFace.addUser(str(uid), info, group, get_file_content('tmp.jpg'))
                        enterFlag = False
                        response = 'finish: info = ' + info
                    else:
                        response = 'no input, retry!'
                elif key == 8:
                    if len(info) >= 1:
                        info = info[:-1]
                    response = info
            else:
                if event.key == ord('l'):
                    led_on = not led_on
                    setLED(led_on)
                    tips = '开灯' if led_on else '关灯'
                    printLine(0,tips)
                elif event.key == ord('a'):
                    printLine(1, '输入')
                    pygame.image.save(image, 'tmp.jpg')
                    enterFlag = True
                    info = ''
                elif event.key == ord('o'):
                    response = '人脸识别'

                elif event.key == ord('v'):
                    recording(True)
                    startRecord()
                elif event.key == ord('q'):
                    camera.stop()
                    pygame.quit()
                    sys.exit()
        elif event.type == KEYUP:
            if event.key == ord('v'):
                recording(False)
                ans = ''
                stopRecord()
                sleep(0.5)
                result = aipSpeech.asr(get_file_content('test.wav'), 'pcm', 16000, {'lan': 'zh',})
                if 'result' in result:
                    speech = result['result'][0].strip(',')
                    printLine(0, speech)
                    if speech in words:
                        words[speech]
                    else:
                        ans = tuling(speech)
                else:
                    ans += '声音不清晰'
                printLine(1, ans)
                text2voice(ans)
        elif event.type == QUIT:
            camera.stop()
            pygame.quit()
            sys.exit()
    




