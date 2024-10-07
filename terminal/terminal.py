import curses


class Terminal:
    def __init__(self, stdscr):
        self.screen = stdscr
        curses.noecho()
        curses.cbreak()

    def kill(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        self.screen.clear()

