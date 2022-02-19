import time
import curses
from curses.textpad import Textbox, rectangle
import RPi.GPIO as GPIO
import time
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)


# stdscr.addstr(0,10,"Hit 'q' to quit")
# stdscr.refresh()

key = None
p = 0
while (key != ord('q')):
    stdscr.refresh()
    stdscr.addstr(0, 0, "                            ")
    stdscr.addstr(0, 0, "Change P, I, or D:")
    key = stdscr.getch()

    if key == ord('P'):
        stdscr.addstr(0, 0, "Change P to what value?")
        editwin = curses.newwin(5,30, 2,1)
        stdscr.refresh()
        box = Textbox(editwin)
        box.edit()
        p = box.gather()
        stdscr.addstr(40, 0, str(p))
        time.sleep(1)
        stdscr.erase()

    if key == ord('I'):
        stdscr.addstr(0, 0, "Change I to what value?")
        editwin = curses.newwin(5,30, 2,1)
        stdscr.refresh()
        box = Textbox(editwin)
        box.edit()
        i = box.gather()
        stdscr.addstr(40, 0, str(i))
        time.sleep(1)
        stdscr.erase()

    if key == ord('D'): 
        stdscr.addstr(0, 0, "Change D to what value?")
        editwin = curses.newwin(5,30, 2,1)
        stdscr.refresh()
        box = Textbox(editwin)
        box.edit()
        d = box.gather()
        stdscr.addstr(40, 0, str(d))
        time.sleep(1)
        stdscr.erase()

            
    
    
