# from time import sleep
# from machine import Pin
# from neopixel import NeoPixel

# led_pin = Pin(48, Pin.OUT)
# led = NeoPixel(led_pin, 1)

# boot_btn = Pin(0, Pin.IN, Pin.PULL_UP)

print("main.py start") # main is running, but not printing

# while boot_btn.value() == 1 :
#     led[0] = (1,1,1)    # LED on
#     led.write()
#     sleep(0.5)
#     led[0] = (0, 0, 0)    # LED off
#     led.write()
#     sleep(0.5)

# exec(open("main.py").read())

led.value(1) # turn off LED

# exec(open("main.py").read())