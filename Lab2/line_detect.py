from TRSensors import TRSensor
from AlphaBot2 import AlphaBot2
import sys, os
import curses
from time import clock
import time
from curses.textpad import Textbox, rectangle
from cursesclass import cursclass

Ab = AlphaBot2()
TR = TRSensor()
C = cursclass()

# Calibrate sensors -> each sensor will output a value between 0 - 1000
for i in range(0, 100):
    if(i < 25 or i >= 75):
        Ab.right()
        Ab.setPWMA(30)
        Ab.setPWMB(30)
    else:
        Ab.left()
        Ab.setPWMA(30)
        Ab.setPWMB(30)
    TR.calibrate()
Ab.stop()

def screen(stdscr):

    height, width = stdscr.getmaxyx()
    center = (width / 2)
    a = width/10
    y = 0
    text = "^"

    while True:
        start_time = time.clock()
        C.screensetup()
        position, Sensors = TR.readLine()

        # Rescale each sensor value from 0 - 1000 to 0 - 40
        s0 = Sensors[0]/25
        s1 = Sensors[1]/25
        s2 = Sensors[2]/25
        s3 = Sensors[3]/25
        s4 = Sensors[4]/25

        # Add to screen the value of each sensor 
        stdscr.addstr(height -1, a*5, str(s0))
        stdscr.addstr(height -1, a*6, str(s1))
        stdscr.addstr(height -1, a*7, str(s2))
        stdscr.addstr(height -1, a*8, str(s3))
        stdscr.addstr(height -1, a*9, str(s4))

        # Calls function addbar from cursesclass on each sensor value
        # Each sensor has its own x cordinate, which is separated by 10 spaces
        # The y cordinate is each sensor's value rescaled.
        C.addbar((height -3) - s0, a*5)
        C.addbar((height -3) - s1, a*6)
        C.addbar((height -3) - s2, a*7)
        C.addbar((height -3) - s3, a*8)
        C.addbar((height -3) - s4, a*9)

        # The position from TR.readline() is rescaled by the width of the screen
        # The value is divided by two to only ouput on the left side of the screen
        x = (float(position) / 4000.0) * width
        x = int(x) / 2

        # Adds the character "^" starting at y postion 0, which is the top of the screen
        # The x coordinate will change depending on the position value
        stdscr.addstr(y, x, text)
        stdscr.refresh()
        # Call refresh() to show the new text on the screen
        time.sleep(0.08)

        # y is incremented by 1 to output the line position moving down the screen
        y = y + 1
        if y == height - 20:
            stdscr.erase()
            y = 0

        # Calls function removebar from cursesclass on each sensor value
        # This function writes blank spaces to the same position addbar wrote to
        C.removebar((height - 3) - s0, a*5)
        C.removebar((height - 3) - s1, a*6)
        C.removebar((height - 3) - s2, a*7)
        C.removebar((height - 3) - s3, a*8)
        C.removebar((height - 3)  -s4, a*9)
        stdscr.refresh()
        # Call refresh to update the screen and overwrite each sensor's previous value position

        end_time = time.clock()
        runtime = str(end_time - start_time)

        stdscr.addstr(height-10,0,"Screen Height:")
        stdscr.addstr(height-10,15,str(height))
        stdscr.addstr(height-8,0,"Screen Width:")
        stdscr.addstr(height-8,14,str(width))

        stdscr.addstr(height-6, 0, "Position Error:")
        stdscr.addstr(height-6, 16, str(position-2000))

        stdscr.addstr(height-4, 0, "Sensor Values:")
        stdscr.addstr(height-4, 15, str(Sensors))
        
        stdscr.addstr(height-2, 0, "Sensor Update Frequency:")
        stdscr.addstr(height-2, 25, runtime)


def main():
    curses.wrapper(screen)

if __name__ == "__main__":
    main()