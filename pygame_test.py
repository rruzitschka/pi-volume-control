import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/raspi-dev/rain.mp3")
pygame.mixer.music.play(-1)

while True:
    time.sleep (60)

pygame.mixer.stop()   
