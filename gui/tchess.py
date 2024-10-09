import pygame as pg
import gui.game as game
import gui.events.event as event
from gui.events.mouse_events import *

class Aplication():
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        pg.init()
        self.FPS = 120
        self.running = True
        self.clicking = False
        self.game = game.Game()
        self.mouseState = [False, False, False]
        self.dragState = {"x": 0, "y": 0, "piece": 0, "offsetX": 0, "offsetY": 0}

    def get_piece_at(self, x: int, y: int):
        x /= 64
        y /= 64
        return self.game.board[8*y+x]


    def update(self):
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
            
            c = pg.mouse.get_pressed()
            for i in range(3):
                if self.mouseState[i] != c[i]: # If the button state is not the same as the one registered last frame, call an event.
                    if c[i]:
                        ClickEvent.call()
                        print(self.get_piece_at(pg.mouse.get_pos()[0], pg.mouse.get_pos([1])))
                    else:
                        ReleaseEvent.call()
                else:
                    DragEvent.call()
                self.mouseState = c

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
            

