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
lock_text = font.render("锁", 1, Color(255, 0, 0))
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
                    if led_on:
                        led_color = Color(255, 255, 255)
                        response = '开灯'
                    else:
                        led_color = Color(100, 100, 100)
                        response = '关灯'
                    pygame.draw.ellipse(sub_right, led_color, led_rect)
                    pygame.display.update(rect_right)
                elif event.key == ord('a'):
                    response = '输入标识'
                    pygame.image.save(image, 'tmp.jpg') 
                    enterFlag = True
                    info = ''
                elif event.key == ord('o'):
                    response = '人脸识别'
                    pygame.image.save(image, 'tmp.jpg')
                    result = aipFace.identifyUser(group, get_file_content('tmp.jpg'))
                    if 'result' in result:
                        item = result['result'][0]
                    
                        info = item['user_info']
                        score = item['scores'][0]
                        response = info + str(score)
                        if score >= 75:
                            pass
                    else:
                        response = 'not found face'
                elif event.key == ord('v'):
                    response = '语音输入'
                    ask = '你：'
                    startRecord()
                elif event.key == ord('q'):
                    camera.stop()
                    pygame.quit()
                    sys.exit()
            res_text = font.render(response, 1, Color(200, 200, 200))
            sub_leftbottom.fill(bg_color, Rect(10,60,620,50))
            sub_leftbottom.blit(res_text, (10, 60))
            pygame.display.update(rect_leftbottom)
        elif event.type == KEYUP:
            if event.key == ord('v'):
                response = ''
                stopRecord()
                sleep(0.5)
                result = aipSpeech.asr(get_file_content('test.wav'), 'pcm', 16000, {'lan': 'zh',})
                if 'result' in result:
                    speech = result['result'][0]
                    ask += speech
                    ans = tuling(speech)
                    response += ans
                    result  = aipSpeech.synthesis(ans, 'zh', 1, {
                        'vol': 5,
                    })
                    print(ans)
                    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
                    if not isinstance(result, dict):
                        with open('audio.mp3', 'wb') as f:
                            f.write(result)
                    time.sleep(0.1)
                    playMp3('audio.mp3')
                else:
                    response += 'not found voice'
            res_text = font.render(response, 1, Color(200, 200, 200))     
            cb_text = font.render(ask, 1, Color(200, 200, 200))
            sub_leftbottom.fill(bg_color, Rect(10,10,620,100))
            sub_leftbottom.blit(res_text, (10, 60))
            sub_leftbottom.blit(cb_text, (10,10))
            pygame.display.update(rect_leftbottom)
        elif event.type == QUIT:
            camera.stop()
            pygame.quit()
            sys.exit()
    




