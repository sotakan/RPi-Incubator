import bme280
import RPi.GPIO as GPIO
import i2clcd
from sys import exit
import threading
import time

str_temp = ""
str_humid = ""
STOP = 0 #Stop signal to send to looping threads

def read_stat(): #Add any other sensors here
    temp,baro,humidity = bme280.readBME280All()
    return [temp,humidity]

#To be used as a thread
def update_lcd(): #This function will regulate the update interval to the lcd so it won't "blink"
    global target_temp, str_temp, str_humid
    while True:
        if STOP == 1:
            break
        str_target = str(target_temp)
        i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target)
        time.sleep(5)
#Thread this thang
def update_sensor(): #This will update the sensor every 5 secs to avoid IOError.
    global temp, humid, str_temp, str_humid, STOP
    try:
        while True:
            stat = read_stat() #stat will retrun as a tuple
            temp = float(round(stat[0], 2)) #Breaking down the tuples...
            humid = float(round(stat[1],2)) #Rounding the float to the 2nd place
            str_temp = str(temp) #The lcd won't take tuples so we will convert them using the str() function.
            str_humid = str(humid)
            time.sleep(5)
            if STOP == 1:
                break
    except(IOError):
        print "Sensor error..."
        i2clcd.main_lcd(ln1="      OFF", ln2="Sensor Error")
        STOP = 1
        GPIO.cleanup()
        exit()


def watchdog():
    global temp, target_temp
    while True:
        if temp < target_temp - 0.15:
            GPIO.output(heatpad_pin,1)
        elif temp > target_temp - 0.14:
            GPIO.output(heatpad_pin,0)
        elif temp > target_temp - 0.5:
            GPIO.output(heatpad_pin,0)

        if STOP == 1:
            break

def init_heat():
    global temp,target_temp
    GPIO.output(heatpad_pin,1)
    while True:
        if temp > target_temp - 1.5:
            GPIO.output(heatpad_pin,0)
            time.sleep(30)
            threading.Thread(target=watchdog).start()
            break


"""
Change these values to match your enviroment!
"""
target_temp = 37.0
heatpad_pin = 7
up_switch_pin = 13
down_switch_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(heatpad_pin, GPIO.OUT)
GPIO.setup(up_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

threading.Thread(target=update_lcd).start()
threading.Thread(target=update_sensor).start()
init_heat()
stat = read_stat()
temp = float(round(stat[0], 2))

try:
    while True:
        if GPIO.input(up_switch_pin) == 1:
            target_temp = target_temp + 0.1
            str_target = str(target_temp)
            i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target)
        elif GPIO.input(down_switch_pin) == 1:
            target_temp = target_temp - 0.1
            str_target = str(target_temp)
            i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target)

except():
    i2clcd.main_lcd(ln1 = "Incubator off", ln2 = "Error")
    STOP = 1
    GPIO.cleanup()
    exit()

except(KeyboardInterrupt):
    i2clcd.main_lcd(ln1 = "Incubator off", ln2 = "KeyboardInterrpt")
    STOP = 1
    GPIO.cleanup()
    exit()
