import RPi.GPIO as GPIO
import time
import vlc
import random
from unittest.mock import patch


SONGPATH='/home/pi/raspi-dev/SoundHelix-Song-1.mp3'
MAXDISTANCE=60   #the maximum distance that I consider


#This set holds the trigger and Echo GPIOs for each connected sensor
#if you one to add a new sensor just add a a tuple to the sensors set
sensors = set()
sensors.add((16,18)) # add first sensor
sensors.add((35,37)) # add second sensor


P=vlc.MediaPlayer(SONGPATH)


def setup():
    GPIO.setmode(GPIO.BOARD)
    for sens in sensors:
        GPIO.setup(sens[0], GPIO.OUT)
        GPIO.setup(sens[1], GPIO.IN)


#this funtion returns the distance from one sensor connected to the respective ports
def single_sensor_distance(trig_port, echo_port):
    GPIO.output(trig_port, 0)
    time.sleep(0.000002)

    GPIO.output(trig_port, 1)
    time.sleep(0.00001)
    GPIO.output(trig_port, 0)


    while GPIO.input(echo_port) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(echo_port) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1

    return during * 340 / 2 * 100


def mock_single_sensor_distance(trig_port, echo_port):
    return random.randrange(3,60)


#collect distance from all sensors and provide it as list
def loop_over_all_sensors():
    distances = set()
    for sens in sensors:
        print("I am in sensor loop for sensor :",sens[0], sens[1])
        x=single_sensor_distance(sens[0], sens[1])
        distances.add(single_sensor_distance(sens[0], sens[1]))

    return distances

#this function returns the aggregated distance value calculated from the distance values received from multiple sensors
#it takes a set of distances as argument and returns a single aggregated distance value

def aggregated_distance(distances):
    
# as a first step this function returns the average distance as reported by the sensor set
# first, add up all the distance values in the set

    sum_distance = 0
    for dis in distances:
            if dis > MAXDISTANCE:
                 dis = MAXDISTANCE
            sum_distance += dis

    aggregated_dis = sum_distance/len(distances)
    return aggregated_dis


#volume calculates the volume based on the distance from the sensor and returns the volume
def volume(dis):

    volume = int (dis/MAXDISTANCE*100)
    return volume



def loop():
    P.play()
    while True:
        # loop over all sensors and collect distances set
        distances = loop_over_all_sensors()
        print("Theses are the individual distances:", distances)
        # calculate the aggregated effective distance
        vol_dis = aggregated_distance(distances)
        print ('Aggregated Distance: %.2f' % vol_dis)
        #set the volume based on the aggregated distance
        result = P.audio_set_volume(volume(vol_dis))
        time.sleep(0.2)

def destroy():
    GPIO.cleanup()
    P.stop()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()