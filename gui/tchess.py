import pygame as pg
import gui.game as game
import gui.events.event as event
from gui.events.mouse_events import *

class Aplication():
    def __init__(self):
        self.size = 64
        self.RES = self.WIDTH, self.HEIGHT = self.size*8, self.size*8
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        pg.init()
        self.FPS = 120
        self.running = True
        self.clicking = False
        self.game = game.Game()
        self.mouseState = [False, False, False, (0, 0)]
        self.dragState = {"x": 0, "y": 0, "piece": 0, "offsetX": 0, "offsetY": 0}
        ClickEvent.addListener(self.onStartDrag, self)

    def get_piece_at(self, pos: tuple[int, int]):
        x = int(pos[0]/64)
        y = int(pos[1]/64)
        i = 8*y+x
        return self.game.board[i] if i >= 0 and i <= 63 else None

    def onStartDrag(self, mouseX: int, mouseY: int, mouseButton: int, piece: int):
        self.dragState["x"] = mouseX
        self.dragState["y"] = mouseY
        self.dragState["piece"] = piece
        print("cacadrag")

    def update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
            
            c = pg.mouse.get_pressed()
            piece = self.get_piece_at(pg.mouse.get_pos())
            for i in range(3):
                if self.mouseState[i] != c[i]: # If the button state is not the same as the one registered last frame, call an event.
                    self.mouseState[i] = c[i]
                    if c[i]:
                        ClickEvent(self.mouseState[3][0], self.mouseState[3][1], i).call()
                    else:
                        ReleaseEvent(self.mouseState[3][0], self.mouseState[3][1], i).call()
                elif c[i]:
                    DragEvent(piece, self.mouseState[3][0], self.mouseState[3][1], i).call()

        # do stuff
        self.render()

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps(), 1)))
        self.clock.tick(self.FPS)

    def render(self):
        col = ((237, 212, 175), (170, 125, 92))
        sqrSize = self.game.boardSize/8
        for y in range(8):
            for x in range(8):
                current_piece = self.game.board[8*y+x]
                pg.draw.rect(self.screen, col[(x+y)%2], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))
                if current_piece != 0:
                    self.screen.blit(self.game.pieces_tex[current_piece], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))
            

