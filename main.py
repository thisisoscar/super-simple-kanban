import pygame as pg

pg.init()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
clock = pg.time.Clock()
font = pg.font.SysFont('nunito', 15) # try kokonor font as well as notosansinscriptionalparthian snd notoserifnyiakengpuachuehmong



running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    


    clock.tick(60)
    pg.display.flip()