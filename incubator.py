
#Ver 0.2 dev 1
import bme280
import RPi.GPIO as GPIO
from i2clcd import main_lcd
import sys
import threading
import time

# I2C LCDs ship with 2 different addresses depending on the lot
try:
    from i2clcd_0x27 import main_lcd
except:
    from i2clcd_0x3f import main_lcd

class hardware:
    # Hardware pins are numbered in BCM
    heatpad_pin = 19
    up_switch_pin = 11
    down_switch_pin = 13

class variables:
    # target_temp here will determine the target on startup
    target_temp = 37.0
    # temp_offset is to eliminate any discrepancies between the sensor readings and actual readings in the box
    temp_offset = 0.0
    temp_visible_offset = 0.0
    # temp and humidity are here because global is ew
    temp = 0.0
    baro = 0.0
    humidity = 0.0
    # implement a kill signal for all looping threads
    kill_thread = False

# Read sensor values and update corresponding data in class variables
def sensor(testing = none):
    if testing == 1:
        try:
            temp,baro,humidity = bme280.readBME280All()
        except IOError:
            print "Error initializing sensor"
            main_lcd(ln1 = "Init Error", ln2 = "Code 1")
            GPIO.cleanup()
            sys.exit()
    elif:
        temp,baro,humidity = bme280.readBME280All()
        # Round values to the 2nd place
        temp = float(round(temp , 2))
        variables.humidity = float(round(humidity , 2))
        # Process offset
        variables.temp = temp - variables.temp_offset
    
def lcd():
    while True:
        sensor()
        main_lcd(ln1 = "Temp: " + str(variables.temp) , ln2 = "Target:" + str(variables.target_temp))
        


def 



# INIT

GPIO.setmode(GPIO.BOARD)
GPIO.setup(hardware.heatpad_pin, GPIO.OUT)
GPIO.setup(hardware.up_switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(hardware.down_switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
>>>>>>> f25c9c18d14a8d41c1ad7d0c3fa44f010163da7a
