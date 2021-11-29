# to test how pygame.mixer.music works



import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/raspi-dev/rain.mp3")
pygame.mixer.music.play(-1)

while True:
    volume=1
    for volume in range(100):
        pygame.mixer.music.set_volume(volume/100)
        print("Volume:", volume)
        time.sleep(2)
 
        
pygame.mixer.stop()   
