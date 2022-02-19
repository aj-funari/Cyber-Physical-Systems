import curses

class cursclass(object):

    def __init__(self):
        self.stdscr = curses.initscr()
        self.height, self.width = self.stdscr.getmaxyx()

    def addbar(self, ypos, xpos):
        try:
            self.stdscr.addstr(ypos, xpos, "^^^^^")
        except curses.error:
            pass

    def removebar(self, ypos, xpos):
        try:
            self.stdscr.addstr(ypos, xpos, "     ")
        except curses.error:
            pass

    def screensetup(self):
        a = self.width / 10
        self.stdscr.addstr(self.height - 2, (a*5), 'Sensor1' )
        self.stdscr.addstr(self.height - 2, (a*6), 'Sensor2' )
        self.stdscr.addstr(self.height - 2, (a*7), 'Sensor3' )
        self.stdscr.addstr(self.height - 2, (a*8), 'Sensor4' )
        self.stdscr.addstr(self.height - 2, (a*9), 'Sensor5' )

        self.stdscr.addstr(40, self.width-3, "0")
        self.stdscr.addstr(30, self.width-3, "10")
        self.stdscr.addstr(20, self.width-3, "20")
        self.stdscr.addstr(10, self.width-3, "30")
        self.stdscr.addstr(0,  self.width-3, "40" )

        for i in range(0, 41):
            self.stdscr.addstr(i, self.width-1, "|")