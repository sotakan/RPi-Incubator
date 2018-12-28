#Ver 0.2dev 1
import bme280
import RPi.GPIO as GPIO
import sys
from threading import Thread
import time


# I2C LCDs ship with 2 different addresses depending on the lot
try:
    try:
        from i2clcd_0x27 import main_lcd, lcd_init
        lcd_init()
    except IOError:
        from i2clcd_0x3f import main_lcd, lcd_init
        lcd_init()
except Exception as e:
    print "Error initializing LCD\nDetails:\n"
    sys.exit()

class hardware:
    # Hardware pins are numbered in BCM
    heatpad_pin                = 19
    up_switch_pin              = 11
    down_switch_pin            = 13
    error_light                = 17
    internet_indicator         = 23
    manual_initiate_ota_update = 27

class variables:
    # target_temp will be set at INIT from file
    target_temp = None
    # temp_offset is to eliminate any discrepancies between the sensor readings and actual readings in the box
    temp_offset = 0.0
    # temp and humidity are here because global is ew
    temp        = 0.0
    baro        = 0.0
    humidity    = 0.0
    # implement a kill signal for all looping threads
    kill_thread = False

# Read sensor values and update corresponding data in class variables
def sensor(testing = None):
    if testing == 1:
        try:
            temp,baro,humidity = bme280.readBME280All()
        except IOError as e:
            print "Error initializing sensor\nDetails:\n"
            print e
            main_lcd(ln1 = "Init Error", ln2 = "Code 1")
            variables.kill_thread = True
            GPIO.cleanup()
            sys.exit()
    else:
        temp,baro,humidity = bme280.readBME280All()
        # Round values to the 2nd place
        temp = float(round(temp , 2))
        variables.humidity = float(round(humidity , 2))
        # Process offset
        variables.temp = temp - variables.temp_offset

def lcd(update = None, custom = False, message1 = None, message2 = None):
    if update == True:
        main_lcd(ln1 = str(variables.temp) + "C ;" + str(variables.humidity) + "%", ln2 = "Target: " + str(variables.target_temp) + "C")
    elif custom == True:
        main_lcd(ln1 = message1, ln2 = message2)

    while True:
        sensor()
        main_lcd(ln1 = str(variables.temp) + "C ;" + str(variables.humidity) + "%", ln2 = "Target: " + str(variables.target_temp) + "C")
        time.sleep(5)
        if variables.kill_thread == True:
            return

# Support OTA updates in the future
def ota():
    pass


# INIT

# Read temp file for target temp
try:
    with open("temp.conf", "r+") as file:
        file = file.read()
        print file
        variables.target_temp = float(round(file, 2))
except IOError:
    with open("temp.conf", "w") as file:
        file.write("37.0")
        variables.target_temp = 37.0
        file.close()


# GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(hardware.heatpad_pin, GPIO.OUT)
GPIO.setup(hardware.up_switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(hardware.down_switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.setup(hardware.manual_initiate_ota_update, GPIO.OUT)
#GPIO.setup(hardware.internet_indicator, GPIO.OUT)

# Test physical connections
sensor(testing = 1)

# Thread LCD
lcd_thread = Thread(target = lcd , args = ())
lcd_thread.daemon = True
lcd_thread.start()

# Wait for sensor to load
time.sleep(2)

# Main

try:
    while True:
        if GPIO.input(hardware.up_switch_pin) == 1:
            variables.target_temp = variables.target_temp + 0.1
            lcd(update = True)
        elif GPIO.input(hardware.down_switch_pin) == 1:
            variables.target_temp = variables.target_temp - 0.1
            lcd(update = True)

        if variables.temp > variables.target_temp:
            GPIO.output(hardware.heatpad_pin, 0)
        elif variables.temp < variables.target_temp:
            GPIO.output(hardware.heatpad_pin, 1)

except KeyboardInterrupt:
    variables.kill_thread = True
    time.sleep(6)
    lcd(custom = True, message1 = "Incubator OFF", message2 = "Manual shutdown")
    with open("temp.conf", "w") as file:
        file.write(str(variables.target_temp))
        file.close()
    GPIO.cleanup()
    sys.exit()

except IOError:
    variables.kill_thread = True
    time.sleep(6)
    lcd(custom = True, message1 = "Incubator OFF", message2 = "IOError")
    with open("temp.conf", "w") as file:
        file.write(str(variables.target_temp))
        file.close()
    GPIO.cleanup()
    sys.exit()

except Exception as e:
    variables.kill_thread = True
    time.sleep(6)
    lcd(custom = True, message1 = "Incubator OFF", message2 = "Unkwn Error")
    print "Error\nDetails:\n" , e
    with open("temp.conf", "w") as file:
        file.write(str(variables.target_temp))
        file.close()
    GPIO.cleanup()
    sys.exit()