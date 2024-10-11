

'''
Change the variable MODE to test either the GUI mode or the Terminal mode
Note that Terminal mode is currently not working well.
'''
MODE = "GUI"


if __name__ == '__main__':
    if MODE == "GUI":
        import gui.tchess as gui
        main = gui.Aplication()
        while main.running:
            main.update()

    elif MODE == "TERMINAL":
        import terminal.tchess as terminal
        terminal.main()
