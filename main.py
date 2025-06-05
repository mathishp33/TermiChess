

'''
Change the variable MODE to test either the GUI mode or the Terminal mode
Note that Terminal mode is currently not working well.
'''
MODE = "GUI"


if __name__ == '__main__':
    BOT = 'ChessAI' #RandBot, ChessAI, None
    BOTMODE = 'load' #create, load
    if MODE == "GUI":
        import gui.tchess as gui

        main = gui.Application(BOT, 'None') #white and black 
        if BOTMODE == 'load':
            import bot.bot as bot
            main.bot, data = bot.ChessAI.load('bot.pckl')
            print(data)
        while main.running:
            main.update()
    elif MODE == "TERMINAL":
        import terminal.tchess as terminal
        terminal.main()
    elif MODE == "TEST":
        import chess.tests.move_generation as mg
        print(mg.test_move_generation(4))
