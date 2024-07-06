# boot.py -- run on boot-up
    ## Original boot file on ESP32 S3 ##
    # This file is executed on every boot (including wake-boot from deepsleep)
    #import esp
    #esp.osdebug(None)
    #import webrepl
    #webrepl.start()

from machine import Pin, reset
import sys

led = Pin(21, Pin.OUT)
    # led.value(0) - LED on
    # led.value(1) - LED off

btn = Pin(0, Pin.IN, Pin.PULL_UP)
    # btn.value() == 0 - button pressed

def reload(mod): # reload module
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)
