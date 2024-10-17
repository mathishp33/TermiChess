#!/usr/bin/env python3

import curses


def loop(screen):
    screen.nodelay(True)
    screen.clear()
    curses.start_color()
    curses.init_pair(12, 0, 7)
    rows, cols = screen.getmaxyx()
    cursor = [rows-1, 2]
    focus = "CMD"
    cmd = ""
    exit = False

    render_pad = curses.newpad(rows - 3, cols)
    cmd_pad = curses.newpad(2, cols)

    cmd_pad.addstr(" " * cols, curses.color_pair(12))
    cmd_pad.addstr("> ")

    screen.refresh()
    render_pad.refresh(0, 0, 0, 0, rows-3, cols)
    cmd_pad.refresh(0, 0, rows-2, 0, rows-1, cols)
    screen.move(cursor[0], cursor[1])

    while not exit:
        screen.noutrefresh()
        try:
            key = screen.getkey()
        except:
            key = ""
        if "KEY" in key:
            if focus == "CMD":
                cursor = _cmd_curmove(cursor, key, cmd, rows, cols)
            screen.move(cursor[0], cursor[1])
            curses.setsyx(cursor[0], cursor[1])
        elif key == "\x7f":
            if focus == "CMD":
                if cursor[1] > 2:
                    cmd = cmd[:cursor[1]-3] + cmd[cursor[1]-2:]
                    cmd_pad.addstr(1, 0, "> "+cmd+" ")
                    cursor[1] -= 1
                    screen.move(cursor[0], cursor[1])
                    cmd_pad.refresh(0, 0, rows-2, 0, rows-1, cols)
        elif key == "\n":
            if focus == "CMD":
                todo = _parse_cmd(cmd, screen)
                if todo == "quit":
                    exit = True
                cmd = ""
                cursor[1] = 2
                cmd_pad.addstr(1, 0, "> "+" "*(rows-2))
                screen.move(cursor[0], cursor[1])
                cmd_pad.refresh(0, 0, rows-2, 0, rows-1, cols)
        elif key != "":
            if focus == "CMD":
                cmd = cmd[:cursor[1]-2] + key + cmd[cursor[1]-2:]
                cmd_pad.addstr(1, 0, "> "+cmd)
                cursor[1] += 1
                screen.move(cursor[0], cursor[1])
                cmd_pad.refresh(0, 0, rows-2, 0, rows-1, cols)
        curses.doupdate()


def _cmd_curmove(cursor: list[int], key: str, cmd: str, rows: int, cols: int):
    if key == "KEY_RIGHT":
        if cursor[1] < len(cmd)+2:
            cursor[1] += 1
    elif key == "KEY_LEFT":
        if cursor[1] > 2:
            cursor[1] -= 1
    return cursor
'''
    elif key == "KEY_UP":
        cursor[0] -= 1
    elif key == "KEY_DOWN":
        cursor[0] += 1
'''

def _parse_cmd(call: str, screen):
    args = call.split(" ")
    cmd = args.pop(0)

    if cmd in ["quit", "q"]:
        return "quit"
    else:
        pass

def main():
    curses.wrapper(loop)


if __name__ == "__main__":
    main()
