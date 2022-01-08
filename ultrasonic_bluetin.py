from Bluetin_Echo import Echo
import RPi.GPIO as GPIO
import time
import pygame
import random
import math
import logging
import plot_volume_curve
from unittest.mock import patch
import os



# Import necessary libraries.
from Bluetin_Echo import Echo

# Define GPIO pin constants.
TRIGGER_PIN_1 = 23
ECHO_PIN_1 = 24
TRIGGER_PIN_2 = 19
ECHO_PIN_2 = 26
# Initialise Sensor with pins, speed of sound.
speed_of_sound = 340
#echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)]
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1) , Echo(TRIGGER_PIN_2, ECHO_PIN_2)]
# Measure Distance 3 times, return average.
samples = 3




SONGPATH='/home/pi/raspi-dev/rain.mp3' #path to the soundfile that is looped
MAXDISTANCE=27   #the maximum distance that I consider
START_VOLUME=0 #the starting volume for the sound player
MAX_VOLUME_STEP=0.05 # how much can the volume change after each measurement cycle
volume_data=[]  # holds the time series of volume data that we use for plotting

# configure the logfile
logging.basicConfig(filename='ultrasonic.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)



pygame.mixer.init() #inits the pygame class


# after startup the PID is written to the file and can be picked up by the monitoring tool
def writePidFile():
    pid = str(os.getpid())
    currentFile = open("ultrasonic.pid", "w")
    currentFile.write(pid)
    currentFile.close()



def setup():
    global echo
    logging.info("##################################################")
    logging.info("Ultrasonic started up")
    logging.info("##################################################")
    # echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)]



def echo_single_sensor_distance(sensor):
       return echo[sensor].read('cm', samples)

#this function just mocks a sensor for testing
def mock_single_sensor_distance(trig_port, echo_port):
    return random.randrange(2,30)


#collect distance from all sensors and provide it as list
def loop_over_all_sensors():
    distances = set()
    for counter in range(0, len(echo)):
        print("I am in sensor loop for sensor :", counter)
        distances.add(echo_single_sensor_distance(counter))

    return distances

#this function returns the aggregated distance value calculated from the distance values received from multiple sensors
#it takes a set of distances as argument and returns a single aggregated distance value

def aggregated_distance(distances):
    
# as a first step this function returns the average distance as reported by the sensor set
# first, add up all the distance values in the set

    sum_distance = 0
    min_distance = MAXDISTANCE
    for dis in distances:
            if dis > MAXDISTANCE:
                 dis = MAXDISTANCE
            if dis < min_distance:
                min_distance = dis
            sum_distance += dis

#    aggregated_dis = sum_distance/len(distances)
# let's try to report always the minimumdistance measured by any sensor
    aggregated_dis = min_distance
    return aggregated_dis


#new_volume calculates the new volume based on the distance from the sensor and returns the volume
#it also smoothes out the volume gradient

def new_volume(current_volume, dis):
    new_volume_from_distance = 1-dis/MAXDISTANCE
    volume = smooth_volume(current_volume, new_volume_from_distance)
    print("CurrentVolume:", current_volume, " New Volume: ", volume)
    return volume


#this function implements the smoothing algorithm
def smooth_volume(current_volume, new_volume):
    dif=new_volume - current_volume
    if math.fabs(dif)>MAX_VOLUME_STEP:
        if dif>0:
            new_volume = current_volume + MAX_VOLUME_STEP
        if dif<0:
            new_volume = current_volume - MAX_VOLUME_STEP
    
    if new_volume>1:
        new_volume=1
    if new_volume<0:
        new_volume=0
    new_volume=round(new_volume,2)
    return new_volume

#main loop
def loop():
    global volume_data
    current_volume=START_VOLUME
    pygame.mixer.music.load(SONGPATH)
    pygame.mixer.music.play(-1)
    while True:
        # loop over all sensors and collect distances set
        distances = loop_over_all_sensors()
        print("Theses are the individual distances:", distances)
        # calculate the aggregated effective distance
        vol_dis = aggregated_distance(distances)
        print ('Aggregated Distance: %.2f' % vol_dis)
        #set the volume based on the aggregated distance
        new_vol=new_volume(current_volume, vol_dis)
        if new_vol != current_volume:
            pygame.mixer.music.set_volume(new_vol)
            logging.info('New Volume set: %s', new_vol)
        else:
            logging.info('No volume change')
        volume_data.append(new_vol)
        current_volume=new_vol
        time.sleep(0.1)

def destroy():
    global echo
    plot_volume_curve.plot_volume(volume_data) #creates the distance graph file volume_graph.png
    echo[0].stop
    pygame.mixer.music.stop()
    logging.info("##################################################")
    logging.info("Ultrasonic terminated orderly")
    logging.info("##################################################")

if __name__ == "__main__":
    writePidFile()
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        # Reset GPIO Pins.

        destroy() 