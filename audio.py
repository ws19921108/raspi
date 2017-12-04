import threading
import pygame
import pyaudio
import wave
import time
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
record_flag = False


def playMp3(filename):
    pygame.mixer.init()
    track = pygame.mixer.music.load(filename)

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.stop()
    
def record():
    global record_flag

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK)

    stream.start_stream()
    print('recording...')
    frames = []
    while record_flag:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print('end')
    wf = wave.open('test.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def startRecord():
    global record_flag
    record_thd = threading.Thread(target=record)
    record_thd.setDaemon(False)
    record_thd.start()
    record_flag= True    

def stopRecord():
    global record_flag
    record_flag= False



