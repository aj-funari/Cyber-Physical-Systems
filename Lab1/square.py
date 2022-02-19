from AlphaBot2 import AlphaBot2
import RPi.GPIO as GPIO
import time


CTR = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)


a = AlphaBot2()
while True:
    if GPIO.input(CTR) == 0:
       
        print("Start your engines!")
        time.sleep(1)
        a.forward()
        time.sleep(1.5)

        print("Turn 1")
        a.right()
        time.sleep(0.15)
        a.forward()
        time.sleep(1.5)

        print("Turn 2")
        a.right()
        time.sleep(0.14)
        a.forward()
        time.sleep(1.5)

        print("Turn 3")
        a.right()
        time.sleep(0.16)
        a.forward()
        time.sleep(1.5)

        print("Last 4")
        a.right()
        time.sleep(0.1)
        a.stop()

        exit()
