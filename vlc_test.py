import vlc
import time

songPath='/home/pi/raspi-dev/SoundHelix-Song-1.mp3'

p=vlc.MediaPlayer(songPath)
p.play()
time.sleep(10)
p.stop()