from AlphaBot2 import AlphaBot2
import RPi.GPIO as GPIO
import curses
import time
from curses.textpad import Textbox, rectangle

class curses_inter(object):
    
    def __init__(self):
        self.stdscr = curses.initscr()
        self.Ab = AlphaBot2() #Initializes AB instance that main program can
        self.key = None
        # self.PID_char = None
        # self.P = 0.1 #Initializing Pterm
        # self.I = 0 #Initializing Iterm
        # self.D = 0 #Initializing Dterm

    def manual(self):
        self.stdscr.keypad(1) #Enables use of special keys like arrow-right.
        # curses.cbreak() #Allows for keys to be pressed without having to press enter to send to the program.
        curses.noecho() #Allows for program to only print keys that are pressed under specific condition I.E if statements.

        self.stdscr.nodelay(True)
        self.key = self.stdscr.getch() #Will return error (-1) if no button is pressed after delay period
        self.stdscr.refresh()

        if self.key == curses.KEY_UP:
            self.stdscr.addstr(1, 1, "                  ") #Clearing screen
            self.stdscr.addstr(1, 1, "Key Pressed: Up")
            self.Ab.forward()
            time.sleep(0.1)
            self.Ab.stop()
        if self.key == curses.KEY_LEFT:
            self.stdscr.addstr(1, 1, "                  ")
            self.stdscr.addstr(1, 1, "Key Pressed: Left")
            self.Ab.left()
            time.sleep(0.1)
            self.Ab.stop()
        if self.key == curses.KEY_RIGHT:
            self.stdscr.addstr(1, 1, "                  ")
            self.stdscr.addstr(1, 1, "Key Pressed: Right")
            self.Ab.right()
            time.sleep(0.1)
            self.Ab.stop()
        if self.key == curses.KEY_DOWN:
            self.stdscr.addstr(1, 1, "                  ")
            self.stdscr.addstr(1, 1, "Key Pressed: Down")
            self.Ab.backward()
            time.sleep(0.1)
            self.Ab.stop()
    
    def checking_keys(self):
        self.stdscr.keypad(1) #Enables use of special keys like arrow-keys.
        # curses.cbreak() #Allows for keys to be pressed without having to press enter to send to the program.
        curses.noecho() #Allows for program to only print keys that are pressed under specific condition I.E if statements.
        
        self.stdscr.nodelay(True)
        self.key = self.stdscr.getch() #Will return error (-1) if no button is pressed after delay period
        self.stdscr.refresh()

        if self.key == ord('m'):  # manual mode
            self.key = 'm'
            return self.key
        if self.key == ord('b'):  # autonomous mode
            self.key = 'b'
            return self.key
        if self.key == ord('q'):  # quit 
            self.key = 'q'
            return self.key
        if self.key == ord('w'):
            self.key = 'w'
            return self.key

    def adjust_PID(self):
        # curses.halfdelay(2)
        # self.stdscr.nodelay(True)
        curses.cbreak()
        curses.noecho()

        self.stdscr.keypad(1)
        self.stdscr.refresh()
        self.stdscr.addstr(2, 50, "                            ")
        self.stdscr.addstr(3, 50, "                            ") #Deleting previous characters
        self.stdscr.addstr(3, 50, "Change P, I, or D:")
        self.PID_char =  self.stdscr.getch() #Fetching character to change

        if self.PID_char == ord('P'): #If term is 'P'
            self.stdscr.addstr(3, 50, "                        ")
            self.stdscr.addstr(3, 50, "Change P to what value?")
            editwin = curses.newwin(5,30, 2,50) #Creating new window 
            self.stdscr.refresh()
            box = Textbox(editwin)
            box.edit()
            self.P = box.gather() #Setting term to whatever integer was typed, then being called back from the main program


        if self.PID_char == ord('I'): #If term is 'I'
            self.stdscr.addstr(3, 50, "                        ")
            self.stdscr.addstr(3, 50, "Change I to what value?")
            editwin = curses.newwin(5,30, 2,50) #Creating new window
            self.stdscr.refresh()
            box = Textbox(editwin)
            box.edit()
            self.I = box.gather() #Setting term to whatever integer was typed, then being called back from the main program


        if self.PID_char == ord('D'): #If term is 'D'
            self.stdscr.addstr(3, 50, "                        ")
            self.stdscr.addstr(3, 50, "Change D to what value?")
            editwin = curses.newwin(5,30, 2,50) #Creating new window
            self.stdscr.refresh()
            box = Textbox(editwin)
            box.edit()
            self.D = box.gather() #Setting term to whatever integer was typed, then being called back from the main program
                