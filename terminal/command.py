import terminal.tchess as t

class Command:
    instance = None
    names: list[str] = []
    def __init__(self):
        Command.instance = self

    def invoke(*args, **kwargs):
        pass

    def get_help():
        t.TerminalApp.instance._print("No help available.")


class Help(Command):
    names = ["help", "h", "?"]

    def invoke(*args, **kwargs):
        if len(args) == 0:
            Help.get_help()
        elif len(args) == 1:
            for cmd in cmds:
                if args[0] in cmd.names:
                    cmd.get_help()
                    return
            t.TerminalApp.instance._error(f"No command named \"{args[0]}\".")
        else:
            t.TerminalApp.instance._error(f"Expected at most 1 argument, but got {len(args)}.")

    def get_help():
        term = t.TerminalApp.instance
        term._print(term._get_centered_text(" Help ", sep="━"), False)
        term._print("", False)
        term._print("- about, more : About Tchess.", False)
        term._print("- clear : Clears the output window.", False)
        term._print("- help, h, ? : Shows the help interface. Use \"help <your cmd>\" to get help on a specific command.", False)
        term._print("- license : The software license", False)
        term._print("- quit, q : Quit Tchess.", False)
        term._print("- restart : Restart Tchess.", False)
        term._print("", False)
        term._print("━"*term.cols)

class About(Command):
    names = ["about", "more"]

    def invoke(*args, **kwargs):
        tm = t.TerminalApp.instance
        if len(args) == 0:
            tm._print(tm._get_centered_text(" About Tchess ", "━"), False)
            tm._print("Tchess is a chess software developed by two 16-year old French students. It is an "
                      "attempt to create a powerful bot with which you can easily interact with, through a "
                      "terminal app or an interface. It is developped in Python.", False)
            tm._print("", False)
            tm._print("All credits go to Noah CAMPAGNE and Mathis HUVER PLANCHON.", False)
            tm._print("━"*tm.cols)
        else:
            tm._error(f"Expected 0 argument, but got {len(args)}.")

class License(Command):
    names = ["license"]

    def invoke(*args, **kwargs):
        tm = t.TerminalApp.instance
        if len(args) == 0:
            tm._print("", False)
            tm._print("MIT License", False)
            tm._print("", False)
            tm._print("Copyright (c) 2024 CAMPAGNE Noah", False)
            tm._print("", False)
            tm._print("Permission is hereby granted, free of charge, to any person obtaining a copy of this "
                      "software and associated documentation files (the \"Software\"), to deal in the Software "
                      "without restriction, including without limitation the rights to use, copy, modify, "
                      "merge, publish, distribute, sublicense, and/or sell copies of the Software, and to "
                      "permit persons to whom the Software is furnished to do so, subject to the following conditions:", False)
            tm._print("", False)
            tm._print("The above copyright notice and this permission notice shall be included in all copies "
                      "or substantial portions of the Software.", False)
            tm._print("", False)
            tm._print("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, "
                      "INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A "
                      "PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT "
                      "HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF "
                      "CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR "
                      "THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
            tm._print("", False)

class Quit(Command):
    names = ["quit", "q"]

    def invoke(*args, **kwargs):
        if len(args) == 0:
            t.TerminalApp.instance.exit = True
        else:
            t.TerminalApp.instance._error(f"Expected 0 argument, but got {len(args)}.")

    def get_help():
        tm = t.TerminalApp.instance
        tm._print(tm._get_centered_text(" Quit Command ", "━"), False)
        tm._print("", False)
        tm._print("On invocation, this command exits the terminal.", False)
        tm._print("Can be called using: quit, q", False)
        tm._print("", False)
        tm._print("━"*tm.cols)

class Restart(Command):
    names = ["restart"]

    def invoke(*args, **kwargs):
        if len(args) == 0:
            t.TerminalApp.instance.exit = True
            t.TerminalApp.instance.restart = True
        else:
            t.TerminalApp.instance._error(f"Expected 0 argument, but got {len(args)}.")

    def get_help():
        tm = t.TerminalApp.instance
        tm._print(tm._get_centered_text(" Restart Command ", "━"), False)
        tm._print("", False)
        tm._print("On invocation, this command restarts Tchess.", False)
        tm._print("Can be called using: restart", False)
        tm._print("", False)
        tm._print("━"*tm.cols)

class Clear(Command):
    names = ["clear"]

    def invoke(*args, **kwargs):
        if len(args) == 0:
            t.TerminalApp.instance.clear_output()
        else:
            t.TerminalApp.instance._error(f"Expected 0 argument, but got {len(args)}.")

    def get_help():
        tm = t.TerminalApp.instance
        tm._print(tm._get_centered_text(" Clear Command ", "━"), False)
        tm._print("", False)
        tm._print("On invocation, this command clears all the output window.", False)
        tm._print("Can be called using: clear", False)
        tm._print("", False)
        tm._print("━"*tm.cols)

class Chess(Command):
    names = ["chess"]

    def invoke(*args, **kwargs):
        tm = t.TerminalApp.instance
        if len(args) == 0:
            tm._error(f"Expected at least 1 argument, but got {len(args)}.")
        else:
            if args[0] == "display":
                tm.render_mode = "BOARD"
                tm.focus = "BOARD"
                tm.set_cur(0)
                tm._refresh_board()
                        

    def get_help():
        tm = t.TerminalApp.instance
        tm._print(tm._get_centered_text(" Chess Command ", "━"), False)
        tm._print("", False)
        tm._print("This command can be used to do various things with the game board.", False)
        tm._print("Can be called using: chess", False)
        tm._print("Usage:", False)
        tm._print("    > chess display|d", False)
        tm._print("        Shows the current state of the board", False)
        tm._print("    > chess get [game|stats|] ...", False)
        tm._print("", False)
        tm._print("━"*tm.cols)


cmds: list[Command.__class__] = [Help, Quit, Clear, Restart, About, License, Chess]