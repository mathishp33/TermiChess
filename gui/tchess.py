import pygame as pg
from pygame.locals import *
import chess.game as game
import gui.events.event as event
from gui.events.mouse_events import *
from gui.events.keyboard_events import *
import chess.utils as utils
import bot.bot as bot

class Application():
    current = None
    def __init__(self, BotMode: str, BotType: str = 'RandBot'):
        Application.current = self
        self.size = 64
        self.RES = self.WIDTH, self.HEIGHT = self.size * 8, self.size * 8
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        pg.init()
        self.FPS = 120
        self.running = True
        self.clicking = False
        self.game = game.Game("GUI")
        self.mouseState = [
            False,  # Left-click state     #0
            False,  # Right-click state    #1
            False,  # Middle-click state   #2
            (0, 0), # Mouse position       #3
            False,  # is dragging ?        #4
            ]
        self.dragState = {"piece": 0, "offsetX": 0, "offsetY": 0, "index": 0, "dragStart": (0, 0)}

        if BotType == 'RandBot':
            self.bot = bot.Randbot(8)
        elif BotType == 'DumbyBot':
            self.bot = bot.DumbyBot(8)

    def get_piece_at(self, pos: tuple[int, int]):
        x = int(pos[0]/64)
        y = int(pos[1]/64)
        i = 8 * y + x
        return self.game.board[i] if i >= 0 and i <= 63 else None
    
    def get_square_at(pos: tuple[int, int]):
        x = int(pos[0]/64)
        y = int(pos[1]/64)
        return (x, y)

    def update(self):
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
            
            if event.type in [pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION, pg.MOUSEWHEEL]:
                c = pg.mouse.get_pressed()
                piece = self.get_piece_at(pg.mouse.get_pos())
                self.mouseState[3] = pg.mouse.get_pos()
                for i in range(3):
                    if self.mouseState[i] != c[i]: # If the button state is not the same as the one registered last frame, call an event.
                        self.mouseState[i] = c[i]
                        if c[i]:
                            EventDispatcher.call_event(MouseClickEvent(self.mouseState[3][0], self.mouseState[3][1], i))
                        else:
                            EventDispatcher.call_event(MouseReleaseEvent(self.mouseState[3][0], self.mouseState[3][1], i))
                    if c[i] and self.mouseState[4]:
                        EventDispatcher.call_event(MouseDragEvent(piece, self.mouseState[3][0], self.mouseState[3][1], i))
                continue

            if event.type == pg.KEYDOWN:
                EventDispatcher.call_event(KeyPressEvent(event.key))
            elif event.type == pg.KEYUP:
                EventDispatcher.call_event(KeyReleaseEvent(event.key))

        # do stuff
        self.render()

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps())))
        self.clock.tick(self.FPS)

    def render(self):
        col = ((237, 212, 175), (170, 125, 92))
        sqrSize = self.game.boardSize/8
        for y in range(8):
            for x in range(8):
                index = 8*y+x
                current_piece = self.game.board[index]
                pg.draw.rect(self.screen, col[(x+y)%2], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))
                if current_piece != 0:
                    if self.mouseState[4]:
                        if index != self.dragState["index"]:
                            self.screen.blit(self.game.pieces_tex[current_piece], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))
                    else:
                        self.screen.blit(self.game.pieces_tex[current_piece], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))

        if self.mouseState[4]:
            self.screen.blit(self.game.pieces_tex[self.dragState["piece"]], pg.Rect(self.mouseState[3][0]+self.dragState["offsetX"]-sqrSize/2, self.mouseState[3][1]+self.dragState["offsetY"]-sqrSize/2, sqrSize/2, sqrSize/2))


@event_listener
def onStartDrag(event: MouseClickEvent):
    piece = Application.current.get_piece_at((event.mouseX, event.mouseY))
    squareX, squareY = Application.get_square_at((event.mouseX, event.mouseY))
    if piece != 0:
        Application.current.mouseState[4] = True
        Application.current.dragState["piece"] = piece
        Application.current.dragState["offsetX"] = 64 * (squareX + 0.5) - event.mouseX
        Application.current.dragState["offsetY"] = 64 * (squareY + 0.5) - event.mouseY
        Application.current.dragState["index"] = 8 * squareY + squareX
        Application.current.dragState["dragStart"] = (squareX, squareY)
    else:
        Application.current.mouseState[4] = False

@event_listener
def onEndDrag(event: MouseReleaseEvent):
    Application.current.mouseState[4] = False
    pos = Application.get_square_at((event.mouseX, event.mouseY))
    if Application.current.dragState["dragStart"] != pos:
        move = game.Move(utils.position_to_index(Application.current.dragState["dragStart"]), utils.position_to_index(pos))
        do_move(move)
        

def do_move(move: game.Move):
    g = game.Game.current
    if move in g.move_generator.moves:
        move.do()
        g.turn = game.BLACK if g.turn == game.WHITE else game.WHITE
        g.move_generator.update_moves(g.turn)
        g.moves.append(move)
        g.move += 1
        if g.turn == Application.current.bot.team:
            to_play = Application.current.bot.think(g.move_generator.moves)
            do_move(to_play)
            