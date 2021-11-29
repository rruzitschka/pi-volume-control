import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/raspi-dev/rain.mp3")
pygame.mixer.music.play(-1)

while True:
   
    for volume in range(100):
        pygame.mixer.set_volume(volume/100)
        time.sleep(5)
    for volume in range(100):
        pygame.mixer.music.set_volume(1 - volume/100)
        time.sleep(5)
        
pygame.mixer.stop()   
