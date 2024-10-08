#!/usr/bin/env python3

import curses


def loop(screen):
    screen.nodelay(True)
    screen.clear()
    curses.start_color()
    curses.init_pair(12, 0, 7)
    rows, cols = screen.getmaxyx()
    cursor = [rows-1, 0]
    focus = "CMD"

    render_pad = curses.newpad(rows - 3, cols)
    cmd_pad = curses.newpad(2, cols)

    cmd_pad.addstr(" " * cols, curses.color_pair(12))

    screen.refresh()
    render_pad.refresh(0, 0, 0, 0, rows-3, cols)
    cmd_pad.refresh(0, 0, rows-2, 0, rows-1, cols)

    while True:
        screen.noutrefresh()
        try:
            key = screen.getkey()
        except:
            key = ""
        if "KEY" in key:
            if key == "KEY_RIGHT":
                cursor[1] += 1
            elif key == "KEY_LEFT":
                cursor[1] -= 1
            elif key == "KEY_UP":
                cursor[0] -= 1
            elif key == "KEY_DOWN":
                cursor[0] += 1
            screen.move(cursor[0], cursor[1])
            curses.setsyx(cursor[0], cursor[1])
        elif key != "":
            if focus == "CMD":
                cmd_pad.addstr(key)
                pass
        curses.doupdate()




def main():
    curses.wrapper(loop)


if __name__ == "__main__":
    main()
