import vlc
import time

p=vlc.MediaPlayer("file:///../SoundHelix-Song-1.mp3")
p.play()
time.sleep(10)
p.stop()