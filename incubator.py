#Ver 0.2 dev 1
import bme280
import RPi.GPIO as GPIO
import i2clcd
from sys import exit
import threading
import time

class hardware:
    # Hardware pins are numbered in BCM
    heatpad_pin = 19
    up_switch_pin = 11
    down_switch_pin = 13

class internal_variables:
    # target_temp here will determine the target on startup
    target_temp = 37.0
    # temp_offset is to eliminate any discrepancies between the sensor readings and actual readings in the box
    temp_offset = 0.0
    # temp and humidity are here just because
    temp = 0.0
    humidity = 0.0
    # implement a kill signal for all looping threads
    kill_thread = False

