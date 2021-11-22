import RPi.GPIO as GPIO
import time
import vlc


SONGPATH='/home/pi/raspi-dev/SoundHelix-Song-1.mp3'
MAXDISTANCE=60   #the maximum distance that I consider
TRIG = 16
ECHO = 18

P=vlc.MediaPlayer(SONGPATH)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


#this funtion cycles through all attached altusonic sensors
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)


    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100


#this function returns the aggregated distance value caluclated from the distance values received from multiple sensors
#simple implementation currently only considers one sensor

def aggregated_distance():
    dis = distance()
    print ('Distance: %.2f' % dis)
    return dis

#volume calculates the volume based on the distance from the sensor
def volume(dis):
    volume = int (dis/MAXDISTANCE*100)
    return volume



def loop():
    P.play()
    while True:
        vol_dis = aggregated_distance()
        print ('Distance: %.2f' % vol_dis)
        result = P.audio_set_volume(volume(vol_dis))
        time.sleep(0.3)

def destroy():
    GPIO.cleanup()
    P.stop()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()