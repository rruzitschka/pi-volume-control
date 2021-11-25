import RPi.GPIO as GPIO
import time
import vlc


SONGPATH='/home/pi/raspi-dev/SoundHelix-Song-1.mp3'
MAXDISTANCE=60   #the maximum distance that I consider
TRIG = 16
ECHO = 18

#This tuple holds the trigger and Echo GPIOs for each connected sensor
#Example for two Ultrasonic sensors: sensors = ((TRIG1,ECHO1), (TRIG2, ECHO2))
sensors = ((16,18))


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

#collect distance from all sensors and provide it as list

def loop_over_all_sensors():
    distances = {}
    for sens in sensors:
        distances.add(single_sensor_distance(sens[0], sens[1]))

    return distances

#this function returns the aggregated distance value calculated from the distance values received from multiple sensors
#it takes a set of distances as argument and returns asingel aggregated distance value
def aggregated_distance(distances):
    
# as a first step this function returns the average distance as reported by the sensor set
# first, add up all the distance values in the set

    sum_distance = 0
    for dis in distances:
            sum_distance += dis

    aggregated_dis = sum_distance/len(distances)
    print ('Aggregated Distance: %.2f' % dis)
    return aggregated_dis


#volume calculates the volume based on the distance from the sensor
def volume(dis):
    volume = int (dis/MAXDISTANCE*100)
    return volume



def loop():
    P.play()
    while True:
        # loop over all sensors and collect distances set
        distances = loop_over_all_sensors()
        print(distances)
        # calculate the aggregated effective distance
        vol_dis = aggregated_distance(distances)
        print ('Distance: %.2f' % vol_dis)
        #set the volume based on the effective distance
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