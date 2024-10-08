import pygame as pg
import gui.game as game

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

    def update(self):
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
            if pg.mouse.get_pressed()[0]:
                self.clicking = True
            else:
                self.clicking = False

        # do stuff
        self.render()

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps(), 1)))
        self.clock.tick(self.FPS)

    def render(self):
        col = ((237, 212, 175), (170, 125, 92))
        sqrSize = self.game.boardSize/8
        for x in range(8):
            for y in range(8):
                pg.draw.rect(self.screen, col[(x+y)%2], pg.Rect(x*sqrSize, y*sqrSize, sqrSize, sqrSize))
            

