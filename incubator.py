import bme280
import RPi.GPIO as GPIO
import i2clcd
from sys import exit
import threading
import time

# Change variables in this class to match your enviroment.
class vars:
    target_temp = 37.0
    temp_offset = 0
    heatpad_pin = 19
    up_switch_pin = 11
    down_switch_pin = 13
    # Don't touch below
    str_temp = ""
    str_humid = ""
    str_target = ""
    STOP = 0 #Stop signal to send to looping threads
    temp = 0
    humid = 0

def read_stat(): #Add any other sensors here
    temp,baro,humidity = bme280.readBME280All()
    return [temp,humidity]

#To be used as a thread
def update_lcd(): #This function will regulate the update interval to the lcd so it won't "blink"
    try:
        while True:
            if vars.STOP == 1:
                exit()
                vars.str_temp = str(vars.temp - vars.temp_offset) #The lcd won't take tuples so we will convert them using the str() function.
                vars.str_humid = str(vars.humid)
                i2clcd.main_lcd(ln1 = "Temp:" + vars.str_temp, ln2 = "Target:" + vars.str_target)
                time.sleep(5)
    except(IOError):
        i2clcd.main_lcd(ln1 = "  LCD Error...", ln2 = "  Resetting...")
        sleep(2)

#Thread this thang
def update_sensor(): #This will update the sensor every 5 secs to avoid IOError.
    while True:
        try:
            stat = read_stat() #stat will retrun as a tuple
            vars.temp = float(round(stat[0], 2)) #Breaking down the tuples...
            vars.humid = float(round(stat[1],2)) #Rounding the float to the 2nd place
            time.sleep(5)
            if vars.STOP == 1:
                exit()
        except(IOError):
            print "Sensor error..."
            i2clcd.main_lcd(ln1="  Sensor Error", ln2="  Resetting...")
            sleep(2)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(vars.heatpad_pin, GPIO.OUT)
GPIO.setup(vars.up_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(vars.down_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

threading.Thread(target=update_lcd).start()
threading.Thread(target=update_sensor).start()
stat = read_stat()
vars.temp = float(round(stat[0], 2))

try:
    while True:
        if GPIO.input(vars.up_switch_pin) == 1:
            vars.target_temp = vars.target_temp + 0.1
            vars.str_target = str(vars.target_temp - vars.temp_offset)
            i2clcd.main_lcd(ln1 = "Temp:" + vars.str_temp, ln2 = "Target:" + vars.str_target)
        elif GPIO.input(vars.down_switch_pin) == 1:
            vars.target_temp = vars.target_temp - 0.1
            vars.str_target = str(vars.target_temp - vars.temp_offset)
            i2clcd.main_lcd(ln1 = "Temp:" + vars.str_temp, ln2 = "Target:" + vars.str_target)
        if vars.temp < vars.target_temp:
            GPIO.output(vars.heatpad_pin,1)
        elif vars.temp > vars.target_temp:
            GPIO.output(vars.heatpad_pin,0)

except():
    i2clcd.main_lcd(ln1 = "Incubator off", ln2 = "Error")
    vars.STOP = 1
    GPIO.cleanup()
    exit()

except(KeyboardInterrupt):
    i2clcd.main_lcd(ln1 = "Incubator off", ln2 = "KeyboardInterrpt")
    vars.STOP = 1
    GPIO.cleanup()
    exit()
