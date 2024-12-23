#!/usr/bin/env python3

import curses
import chess.game as game
import terminal.command as commands
import math

class TerminalApp():
    instance = None
    
    def main(self, screen):
        TerminalApp.instance = self
        self.game = game.Game("TERMINAL")
        self.screen = screen
        self.screen.nodelay(True)
        self.screen.clear()
        curses.start_color()

        curses.init_pair(18, 0, 7) 
        curses.init_pair(28, 1, 7)
        curses.init_pair(21, 1, 0) # RED
        curses.init_pair(31, 2, 0) # GREEN
        curses.init_pair(41, 3, 0) # YELLOW
        curses.init_pair(51, 4, 0) # BLUE
        curses.init_pair(61, 5, 0) # PURPLE
        curses.init_pair(71, 6, 0) # AQUA
        curses.init_pair(81, 7, 0) # WHITE

        self.rows, self.cols = screen.getmaxyx()
        self.cursor = [self.rows-1, 2]
        self.focus = "CMD"
        self.cmd = ""
        self.exit = False
        self.restart = False
        self.output: list[str | tuple[str, int]] = []
        self.cmd_history = [""]
        self.cmd_i = 0
        self.render_mode = "OUTPUT"
        self.board_cursor = [0, 0]

        self.render_pad = curses.newpad(self.rows - 2, self.cols)
        self.cmd_pad = curses.newpad(2, self.cols)

        self._print(self._get_centered_text(" Tchess "), False, curses.color_pair(71))
        self._print(self._get_centered_text(" An interactive terminal application specialized for chess "), False)
        self._print("━"*self.cols)

        self.cmd_pad.addstr(" " * self.cols, curses.color_pair(18))
        self.cmd_pad.addstr("> ")

        self.refresh((1, 1, 1))
        self.screen.move(self.cursor[0], self.cursor[1])

        self.loop()

    def loop(self):
        while not self.exit:
            self.screen.noutrefresh()
            try:
                key = self.screen.getkey()
            except:
                key = ""
            if "KEY" in key:
                if self.focus == "CMD":
                    self._cmd_curmove(key)
                elif self.focus == "BOARD":
                    self._board_curmove(key)
                self.screen.move(self.cursor[0], self.cursor[1])
                curses.setsyx(self.cursor[0], self.cursor[1])
            elif key == "\x7f":
                if self.focus == "CMD":
                    if self.cursor[1] > 2:
                        self.cmd = self.cmd[:self.cursor[1]-3] + self.cmd[self.cursor[1]-2:]
                        self.cmd_pad.addstr(1, 0, "> "+self.cmd+" ")
                        self.cursor[1] -= 1
                        self.screen.move(self.cursor[0], self.cursor[1])
                        self.refresh((0, 1, 0))
            elif key == "\n":
                if self.focus == "CMD":
                    self._parse_cmd(self.cmd)
                    if self.cmd != "":
                        self.cmd_history[len(self.cmd_history)-1] = self.cmd
                        self.cmd = ""
                        self.cmd_i = len(self.cmd_history)
                        self.cmd_history.append("")
                        self.cursor[1] = 2
                        self.cmd_pad.addstr(1, 0, "> "+" "*(self.cols-3))
                        self.screen.move(self.cursor[0], self.cursor[1])
                        self.refresh((0, 1, 0))
                    else:
                        self.cmd_i = len(self.cmd_history)-1
            elif key == "\t":
                if self.focus == "CMD":
                    self.focus = "BOARD"
                    self.set_cur(0)
                elif self.focus == "BOARD":
                    self.focus = "CMD"
                    self.set_cur(1)
            elif key != "":
                if self.focus == "CMD":
                    self.cmd = self.cmd[:self.cursor[1]-2] + key + self.cmd[self.cursor[1]-2:]
                    self.cmd_pad.addstr(1, 0, "> "+self.cmd)
                    self.cursor[1] += 1
                    self.screen.move(self.cursor[0], self.cursor[1])
                    self.refresh((0, 1, 0))
                elif key == ":":
                    self.focus = "CMD"
                    self.set_cur(1)
                elif self.focus == "BOARD":
                    if key == "x":
                        self.render_mode = "OUTPUT"
                        self.focus = "CMD"
                        self.set_cur(1)
                        self._refresh_output()
            curses.doupdate()
        if self.restart:
            self.restart = False
            self.main(self.screen)

    def refresh(self, flags: tuple[bool, bool, bool, bool]):
        if flags[0]: self.screen.refresh()
        if flags[1]: self.cmd_pad.refresh(0, 0, self.rows-2, 0, self.rows-1, self.cols)
        if flags[2]: self.render_pad.refresh(0, 0, 0, 0, self.rows-3, self.cols)

    def clear_output(self):
        self.output.clear()
        self._refresh_output()

    def _parse_cmd(self, call: str):
        args = call.split(" ")
        cmd = args.pop(0)

        if cmd == "":
            return
        self._print("> " + self.cmd)

        for command in commands.cmds:
            if cmd in command.names:
                command.invoke(*args)
                return
        self._error("Unknown command: "+cmd)

    def _refresh_output(self):
        if self.render_mode == "OUTPUT":
            self.render_pad.clear()

            begin = max(0, len(self.output) - (self.rows - 3))
            for i in range(begin, len(self.output)):
                if type(self.output[i]) == str:
                    self.render_pad.addstr(i-begin, 0, self.output[i])
                else:
                    self.render_pad.addstr(i-begin, 0, self.output[i][0], self.output[i][1])

        self.refresh((0, 0, 1))

    def _refresh_board(self):
        if self.render_mode == "BOARD":
            self.render_pad.clear()
            self._draw_board(3, 1)
            self.render_pad.addstr(self.rows-3, 0, "x: exit")
            self.refresh((0, 0, 1, 0))

    def _draw_board(self, sqrwidth: int, sqrheight: int):
        self.render_pad.addstr("┏" + "━" * sqrwidth + ("┳" + "━" * sqrwidth) * 7 + "┓\n")
        for i in range(sqrheight):
            if i == math.floor(sqrheight/2):
                self.render_pad.addstr(("┃" + " " * sqrwidth) * 8 + "┃ 8\n")
            else:
                self.render_pad.addstr(("┃" + " " * sqrwidth) * 8 + "┃\n")
        for i in range(7):
            self.render_pad.addstr("┣" + "━" * sqrwidth + ("╋" + "━" * sqrwidth) * 7 + "┫\n")
            for j in range(sqrheight):
                if j == math.floor(sqrheight/2):
                    self.render_pad.addstr(("┃" + " " * sqrwidth) * 8 + "┃ " + str(7-i) + "\n")
                else:
                    self.render_pad.addstr(("┃" + " " * sqrwidth) * 8 + "┃\n")
        self.render_pad.addstr("┗" + "━" * sqrwidth + ("┻" + "━" * sqrwidth) * 7 + "┛\n" + " " * math.floor((sqrwidth/2)+1))
        for i in range(8):
            self.render_pad.addstr(chr(97+i) + " " * sqrwidth)

        x = math.ceil(sqrwidth/2)
        y = math.ceil(sqrheight/2)

        for iy in range(8):
            for ix in range(8):
                self.render_pad.addstr(y, x, game.Game.get_char_from_piece(self.game.board[8*iy+ix]), curses.A_REVERSE if [iy, ix] == self.board_cursor else 0)
                x += sqrwidth + 1
            x = math.ceil(sqrwidth/2)
            y += sqrheight + 1



    def _print(self, msg: str, refresh: bool = True, color_pair: int = -1):
        if color_pair == -1:
            for m in self._cut([msg]):
                self.output.append(m)
        else:
            for m in self._cut([msg]):
                self.output.append((m, color_pair))
        if refresh: self._refresh_output()

    def _error(self, msg: str, refresh: bool = True):
        for m in self._cut([msg]):
            self.output.append((m, curses.color_pair(21)))
        if refresh: self._refresh_output()

    def _get_centered_text(self, text: str, sep: str = " "):
        s = sep * (len(text)%2 + int(((self.cols-len(text))/2))) + text + sep * int(((self.cols-len(text))/2))
        return s[:self.cols]
    
    def _cut(self, text: list[str]) -> list[str]:
        last = text[len(text)-1]
        if len(last) > self.cols:
            text.pop()
            return text + [last[:self.cols]] + self._cut([last[self.cols:].lstrip()])
        else:
            return text
        
    def set_cur(self, mode: int):
        return curses.curs_set(mode)
        
    def _cmd_curmove(self, key: str):
        if key == "KEY_RIGHT":
            if self.cursor[1] < len(self.cmd)+2:
                self.cursor[1] += 1
        elif key == "KEY_LEFT":
            if self.cursor[1] > 2:
                self.cursor[1] -= 1
        elif key == "KEY_UP":
            if self.cmd_i > 0:
                self.cmd_i -= 1
                self.cmd = self.cmd_history[self.cmd_i]
                self.cmd_pad.addstr(1, 0, "> " + " "*(self.cols-3))
                self.cmd_pad.addstr(1, 0, "> "+self.cmd)
                self.cursor[1] = 2 + len(self.cmd)
                self.refresh((0, 1, 0))
        elif key == "KEY_DOWN":
            if self.cmd_i < len(self.cmd_history)-1:
                self.cmd_i += 1
                self.cmd = self.cmd_history[self.cmd_i]
                self.cmd_pad.addstr(1, 0, "> " + " "*(self.cols-3))
                self.cmd_pad.addstr(1, 0, "> "+self.cmd)
                self.cursor[1] = 2 + len(self.cmd)
                self.refresh((0, 1, 0))
        return self.cursor
    
    def _board_curmove(self, key: str):
        if key == "KEY_RIGHT":
            if self.board_cursor[1] < 7:
                self.board_cursor[1] += 1
        elif key == "KEY_LEFT":
            if self.board_cursor[1] > 0:
                self.board_cursor[1] -= 1
        elif key == "KEY_UP":
            if self.board_cursor[0] > 0:
                self.board_cursor[0] -= 1
        elif key == "KEY_DOWN":
            if self.board_cursor[0] < 7:
                self.board_cursor[0] += 1
        self._refresh_board()
        return self.board_cursor


def main():
    curses.wrapper(TerminalApp().main)


if __name__ == "__main__":
    main()
