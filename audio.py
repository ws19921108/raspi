from time import sleep
import pygame
import pyaudio
import wave

file='audio.mp3'
pygame.mixer.init()
print("播放音乐1")
track = pygame.mixer.music.load(file)

pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass
pygame.mixer.music.stop()

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
TIME = 5
# define callback (2)
def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)


frames = []
# open stream using callback (3)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while TIME:
    sleep(1)
    TIME -= 1

# stop stream (6)
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open('audio.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# close PyAudio (7)
