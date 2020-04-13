#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
#set servo Pins
servoPIN = 17
#set flow Pins
inpt = 13
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(servoPIN,GPIO.OUT)
GPIO.setup(inpt,GPIO.IN)

#inisialisasi servo
p=GPIO.PWM(18,50)
p.start(2.5)

#inisialisasi flow 
rate_cnt = 0
tot_cnt = 0
minutes = 0
constant = 0.10
time_new = 0.0

print('start')
print('Control C to exit')


def flowmeter():
    while True:
        time_new = time.time() +10
        rate_cnt = 0
        while time.time() <= time_new:
            if GPIO.input(inpt)!= 0:
               rate_cnt += 1
               tot_cnt += 1
            try:
               print(GPIO.input(inpt), end=='')
            except KeyboardInterrupt:
               print('\nCTRL C - Exiting nicely')
               GPIO.cleanup()
               sys.exit()
               
        minutes += 1
        print('\nLiters / min', round(rate_cnt * constant,4))
        print('Total Liters', round(tot_cnt * constant,4))
        print('Time (min&clock)', minutes, '\t', time.asctime(time.localtime(time.time())),'\n')

    GPIO.cleanup()
    print('done')

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
 
def servo_movement():
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)            

    try:
        while True:
            if dist == 20 :
                p.ChangeDutyCycle(20)
                time.sleep(0.2)
            if dist == 40 :
                p.ChangeDutyCycle(20)
                time.sleep(0.2)
            if dist == 60 :
                p.ChangeDutyCycle(20)
                time.sleep(0.2)
            if dist == 80 :
                p.ChangeDutyCycle(20)
                time.sleep(0.2)
            time.sleep(0.1) 
    

    except KeyboardInterrupt:
        flowmeter()
        distance()
        servo_movement()
        print ('Quit')
        GPIO.cleanup()
        exit()
        
