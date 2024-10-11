import pygame as pg
import gui.game as game

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
        self.mouse_pos = (0, 0)
        self.game = game.Pieces()
        self.select = (0, 0)

    def update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
                pg.quit()
        if pg.mouse.get_pressed()[0]:
            self.clicking = True
        else:
            self.clicking = False 
        if self.clicking:
            for i in self.game.pieces:
                idle = pg.Rect(i[0]*self.size, i[1]*self.size, self.size, self.size)
                if idle.collidepoint(self.mouse_pos):
                    self.select = (i[0]*self.size, i[1]*self.size)
                    moves = self.game.board.moves[str(i[3])]
                    for j in moves[0]:
                        if moves[1] == 1:
                            for k in range(moves[2], 0, -1): 
                                pg.draw.circle(self.screen, (255, 255, 255), (self.select[0]+k*self.size, self.select[1]+k*self.size), 20)
                                pg.display.update(pg.draw.circle(self.screen, (255, 255, 255), (self.select), 20))
                                print(self.select[0]+k, self.select[1]+k)
                    while True:
                        self.mouse_pos = pg.mouse.get_pos()
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                    


        # do stuff
        self.drawing(50)

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps(), 1)))
        self.clock.tick(self.FPS)

    def drawing(self, a):
        colors = ((237, 212, 175), (170, 125, 92))
        for i in range(8):
            for j in range(8):
                pg.draw.rect(self.screen, colors[(i+j)%2], pg.Rect(self.size*i, self.size*j, self.size, self.size))
                
        for i in self.game.pieces:
            idle = i[2].get_rect(center=(i[0]*self.size+self.size/2, i[1]*self.size+self.size/2))
            self.screen.blit(i[2], idle)
