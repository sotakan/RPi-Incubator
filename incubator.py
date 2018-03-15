import bme280
import RPi.GPIO as GPIO
import i2clcd
from sys import exit
import threading
import time

str_temp = ""
str_humid = ""
STOP = 0 #Stop signal to send to looping threads
view_mode = 0 #This will toggle between temperature(0) or humidity(1)

def read_stat(): #Add any other sensors here
    temp,baro,humidity = bme280.readBME280All()
    return [temp,humidity]

#To be used as a thread
#Thread this thang
def update_sensor(): #This will update the sensor and lcd every 5 secs to avoid IOError.
    global temp, humid, target_temp, target_humid, str_target_temp, str_target_humid, STOP
    try:
        while True:
            stat = read_stat() #stat will retrun as a tuple
            temp = float(round(stat[0], 2)) #Breaking down the tuples...
            humid = float(round(stat[1],2)) #Rounding the float to the 2nd place
            if view_mode == 0:
                str_temp = str(temp) #The lcd won't take tuples so we will convert them using the str() function.
                str_target_temp = str(target_temp)
                i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target_temp)
            elif view_mode == 1:
                str_humid = str(humid)
                str_target_humid = str(target_humid)
                i2clcd.main_lcd(ln1 = "Humidity:" + str_humid, ln2 = "Target:" + str_target_humid)
            time.sleep(5)
            if STOP == 1:
                exit()
    except(IOError):
        print "Sensor error..."
        i2clcd.main_lcd(ln1="      OFF", ln2="Sensor Error")
        STOP = 1
        GPIO.cleanup()
        exit()

def humidity_watch():
    global humid, target_humid, STOP
    while True:
        if STOP == 1:
            exit()
        if humid < target_humid:
            GPIO.output(spray_motor_pin, 1)
            time.sleep(5) #Spray water for 5 seconds
            GPIO.output(spray_motor_pin, 0)
            time.sleep(180) #We will wait 2 minutes for the water to evapotate


"""
Change these values to match your enviroment!
"""
target_temp = 37.0
target_humid = 50.0
heatpad_pin = 11
spray_motor_pin = 19
up_switch_pin = 13
down_switch_pin = 15
toggle_view_pin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(heatpad_pin, GPIO.OUT)
GPIO.setup(spray_motor_pin, GPIO.OUT)
GPIO.setup(up_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(toggle_view_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Starting thread
threading.Thread(target=update_sensor).start()
threading.Thread(target=humidity_watch).start()

try:
    while True:
        if GPIO.input(up_switch_pin) == 1:
            if view_mode == 0:
                target_temp = target_temp + 0.1
                str_target_temp = str(target_temp)
                i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target_temp)
            elif view_mode == 1:
                target_humid = target_humid + 0.1
                str_target_humid = str(target_humid)
                i2clcd.main_lcd(ln1 = "Humidity:" + str_humid, ln2 = "Target:" + str_target_humid)

        elif GPIO.input(down_switch_pin) == 1:
            if view_mode == 0:
                target_temp = target_temp - 0.1
                str_target_temp = str(target_temp)
                i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target_temp)
            elif view_mode == 1:
                target_humid = target_humid - 0.1
                str_target_humid = str(target_humid)
                i2clcd.main_lcd(ln1 = "Humidity:" + str_humid, ln2 = "Target:" + str_target_humid)

        elif GPIO.input(toggle_view_pin) == 1 and view_mode == 0: #If it was in temperature mode
            view_mode == 1
            i2clcd.main_lcd(ln1 = "Humidity:" + str_humid, ln2 = "Target:" + str_target_humid)
        elif GPIO.input(toggle_view_pin) == 1 and view_mode == 1:
            view_mode == 0
            i2clcd.main_lcd(ln1 = "Temp:" + str_temp, ln2 = "Target:" + str_target_temp)

        if temp < target_temp:
            GPIO.output(heatpad_pin,1)
        elif temp > target_temp:
            GPIO.output(heatpad_pin,0)

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
