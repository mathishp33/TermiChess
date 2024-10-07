import gui.tchess as gui
import terminal.tchess as terminal


'''
Change the variable MODE to test either the GUI mode or the Terminal mode
Note that Terminal mode is currently not working well.
'''
MODE = "GUI"


if __name__ == '__main__':
    if MODE == "GUI":
        main = gui.Aplication()
        while main.running:
            main.update()

    elif MODE == "TERMINAL":
        terminal.main()
