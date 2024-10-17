#!/usr/bin/env python3

import curses

class TerminalApp():
    def main(self, screen):
        self.screen = screen
        self.screen.nodelay(True)
        self.screen.clear()
        curses.start_color()

        curses.init_pair(18, 0, 7)
        curses.init_pair(28, 1, 7)
        curses.init_pair(21, 1, 0)

        self.rows, self.cols = screen.getmaxyx()
        self.cursor = [self.rows-1, 2]
        self.focus = "CMD"
        self.cmd = ""
        self.exit = False
        self.output: list[str | tuple[str, int]] = []

        self.render_pad = curses.newpad(self.rows - 2, self.cols)
        self.cmd_pad = curses.newpad(2, self.cols)

        self._print(self._get_centered_text(" Tchess "), False)
        self._print(self._get_centered_text(" An interactive terminal application specialized for chess "), False)
        self._print("–"*self.cols)

        self.cmd_pad.addstr(" " * self.cols, curses.color_pair(18))
        self.cmd_pad.addstr("> ")

        self._refresh((1, 1, 1))
        self.screen.move(self.cursor[0], self.cursor[1])

        while not self.exit:
            self.screen.noutrefresh()
            try:
                key = screen.getkey()
            except:
                key = ""
            if "KEY" in key:
                if self.focus == "CMD":
                    self.cursor = self._cmd_curmove(key)
                self.screen.move(self.cursor[0], self.cursor[1])
                curses.setsyx(self.cursor[0], self.cursor[1])
            elif key == "\x7f":
                if self.focus == "CMD":
                    if self.cursor[1] > 2:
                        self.cmd = self.cmd[:self.cursor[1]-3] + self.cmd[self.cursor[1]-2:]
                        self.cmd_pad.addstr(1, 0, "> "+self.cmd+" ")
                        self.cursor[1] -= 1
                        self.screen.move(self.cursor[0], self.cursor[1])
                        self._refresh((0, 1, 0))
            elif key == "\n":
                if self.focus == "CMD":
                    self._parse_cmd(self.cmd)
                    self.cmd = ""
                    self.cursor[1] = 2
                    self.cmd_pad.addstr(1, 0, "> "+" "*(self.rows-2))
                    self.screen.move(self.cursor[0], self.cursor[1])
                    self._refresh((0, 1, 0))
            elif key != "":
                if self.focus == "CMD":
                    self.cmd = self.cmd[:self.cursor[1]-2] + key + self.cmd[self.cursor[1]-2:]
                    self.cmd_pad.addstr(1, 0, "> "+self.cmd)
                    self.cursor[1] += 1
                    self.screen.move(self.cursor[0], self.cursor[1])
                    self._refresh((0, 1, 0))
            curses.doupdate()


    def _cmd_curmove(self, key: str):
        if key == "KEY_RIGHT":
            if self.cursor[1] < len(self.cmd)+2:
                self.cursor[1] += 1
        elif key == "KEY_LEFT":
            if self.cursor[1] > 2:
                self.cursor[1] -= 1
        return self.cursor
    '''
        elif key == "KEY_UP":
            cursor[0] -= 1
        elif key == "KEY_DOWN":
            cursor[0] += 1
    '''

    def _parse_cmd(self, call: str):
        args = call.split(" ")
        cmd = args.pop(0)

        if cmd == "":
            return
        self._print("> " + self.cmd)

        if cmd in ["quit", "q"]:
            self.exit = True
        elif cmd in ["help", "h", "?"]:
            self._print(self._get_centered_text(" Help ", sep="–"), False)
            self._print("", False)
            self._print("- clear : Clears the output window.", False)
            self._print("- help, h, ? : Shows the help interface. Use \"help <your cmd>\" to get help on a", False)
            self._print("specific command.", False)
            self._print("- quit, q : Quit Tchess.", False)
            self._print("", False)
            self._print("–"*self.cols)
        elif cmd == "clear":
            self._clear_output()
        else:
            self._error("Unknown command: "+cmd)

    def _refresh(self, flags: tuple[bool, bool, bool]):
        if flags[0]: self.screen.refresh()
        if flags[1]: self.cmd_pad.refresh(0, 0, self.rows-2, 0, self.rows-1, self.cols)
        if flags[2]: self.render_pad.refresh(0, 0, 0, 0, self.rows-3, self.cols)

    def _refresh_output(self):
        self.render_pad.clear()

        begin = max(0, len(self.output) - (self.rows - 3))
        for i in range(begin, len(self.output)):
            if type(self.output[i]) == str:
                self.render_pad.addstr(i-begin, 0, self.output[i])
            else:
                self.render_pad.addstr(i-begin, 0, self.output[i][0], self.output[i][1])

        self._refresh((0, 0, 1))

    def _print(self, msg: str, refresh: bool = True):
        self.output.append(msg)
        if refresh: self._refresh_output()

    def _error(self, msg: str, refresh: bool = True):
        self.output.append((msg, curses.color_pair(21)))
        if refresh: self._refresh_output()

    def _clear_output(self):
        self.output.clear()
        self._refresh_output()

    def _get_centered_text(self, text: str, sep: str = " "):
        return sep * int(((self.cols-len(text))/2)) + text + sep * int(((self.cols-len(text))/2))


def main():
    curses.wrapper(TerminalApp().main)


if __name__ == "__main__":
    main()
