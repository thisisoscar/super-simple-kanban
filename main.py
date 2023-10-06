import pygame as pg

pg.init()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
clock = pg.time.Clock()
title_font = pg.font.SysFont('arial', 40) # nunito kokonor notosansinscriptionalparthian notoserifnyiakengpuachuehmong
big_border_width = 3

def draw_section_titles():
    n_sections = len(kanban_data)
    
    text_surfaces = [title_font.render(i, True, (255,255,255)) for i in list(kanban_data)]
    
    text_distances = screen_width // (n_sections)

    x_pos = 0

    for surface in text_surfaces:
        x_pos += text_distances

        text_width = surface.get_width()

        adjustment = text_distances // 2

        text_rect = surface.get_rect()
        text_rect.midtop = (x_pos-adjustment, 0)

        screen.blit(surface, text_rect)
    
    return text_surfaces


def draw_vertical_borders():
    n_sections = len(kanban_data)

    border_distances = screen_width // n_sections

    x_pos = 0

    for _ in range(n_sections-1):
        x_pos += border_distances

        pg.draw.line(screen, (255,255,255), (x_pos,0), (x_pos,screen_height), big_border_width)

def draw_horizontal_border(text_surfaces):
    max_height = max([i.get_height() for i in text_surfaces])
    
    pg.draw.line(screen, (255,255,255), (0,max_height), (screen_width,max_height), big_border_width)


kanban_data = {'to do':[], 'in progess':[], 'done':[]}

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    
    text_surfaces = draw_section_titles()
    draw_vertical_borders()
    draw_horizontal_border(text_surfaces)

    clock.tick(60)
    pg.display.flip()