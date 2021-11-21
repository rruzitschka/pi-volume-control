import vlc
import time

songPath='/home/pi/raspi-dev/SoundHelix-Song-1.mp3'

p=vlc.MediaPlayer(songPath)
p.play()
for i in range(100):
    result = p.audio_set_volume(i)
    print("Volume:",i, "result:", result)
    time.sleep(2)
time.sleep(10)
p.stop()