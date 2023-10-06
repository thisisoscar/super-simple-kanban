import pygame as pg

pg.init()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
clock = pg.time.Clock()
title_font = pg.font.SysFont('chalkduster', 40)
text_font = pg.font.SysFont('chalkduster', 20)
big_border_width = 3
small_border_width = 1
box_margin = 15
box_padding = 15
selected = None

class Task:
    def __init__(self, text, category):
        self.text = text
        self.category = category
        self.height = self.get_height()
        self.rect = None
        self.background_colour = (100,100,100)
    
    def draw(self):
        text_surface = text_font.render(self.text, True, (255,255,255), wraplength=int(get_section_distances()/1.2))
        
        height = text_surface.get_height() + (box_margin * 2)
        width = get_section_distances() // 1.2
        
        surface = pg.Surface((width, height))
        surface.fill(self.background_colour)
        surface.blit(text_surface, (box_margin,box_margin))
        
        x_pos = self.category.index * get_section_distances()
        x_pos -= get_section_distances() // 2

        y_pos = self.get_y_position()

        self.rect = surface.get_rect(midtop=(x_pos, y_pos))
        
        screen.blit(surface, self.rect)
    
    def get_height(self):
        text_surface = text_font.render(self.text, True, (255,255,255), wraplength=int(get_section_distances()/1.2))
        height = text_surface.get_height() + (box_margin * 2)

        return height
    
    def get_y_position(self):
        y_pos = 100

        for i in self.category.tasks:
            if i == self:
                break
            else:
                y_pos += i.height
                y_pos += box_padding
        
        return y_pos


class Category:
    def __init__(self, text, index):
        self.text = text
        self.index = index
        self.tasks = []


def create_task(task_text, category):
    task = Task(task_text, category)
    kanban_data[category].append(task)
    category.tasks.append(task)


def get_section_distances():
    n_sections = len(kanban_data)
    distance = screen_width // n_sections

    return distance


def draw_section_titles():
    title_text_surfaces = [title_font.render(i.text, True, (255,255,255)) for i in list(kanban_data)]
    
    text_distances = get_section_distances()

    x_pos = 0

    for surface in title_text_surfaces:
        x_pos += text_distances

        adjustment = text_distances // 2

        text_rect = surface.get_rect()
        text_rect.midtop = (x_pos-adjustment, 0)

        screen.blit(surface, text_rect)
    
    return title_text_surfaces


def draw_vertical_borders():
    border_distances = get_section_distances()

    n_sections = len(kanban_data)

    x_pos = 0

    for _ in range(n_sections-1):
        x_pos += border_distances

        pg.draw.line(screen, (255,255,255), (x_pos,0), (x_pos,screen_height), big_border_width)


def draw_horizontal_border(text_surfaces):
    max_height = max([i.get_height() for i in text_surfaces])
    
    pg.draw.line(screen, (255,255,255), (0,max_height), (screen_width,max_height), big_border_width)


kanban_data = {Category(text='to do', index=1):[], Category(text='in progress', index=2):[], Category(text='done', index=3):[]}

create_task('start it', list(kanban_data)[0])
create_task('finish it so that i can sleep at night lmaoi', list(kanban_data)[0])

running = True
while running:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        
        if event.type == pg.MOUSEBUTTONDOWN:
            for category in kanban_data:
                for task in kanban_data[category]:
                    if task.rect.collidepoint(event.pos):
                        selected = task
                        task.background_colour = (50,50,200)
                        break
                    
        if event.type == pg.MOUSEBUTTONUP and selected != None:
            section_distances = get_section_distances()
            index = 0
            x_val = 0
            while x_val < event.pos[0]:
                x_val += section_distances
                index += 1

            category = list(kanban_data)[index-1]
            selected.background_colour = (100,100,100)
            selected.category.tasks.remove(selected)
            category.tasks.append(selected)
            selected.category = category
            selected = None
    
    title_text_surfaces = draw_section_titles()
    draw_vertical_borders()
    draw_horizontal_border(title_text_surfaces)
    for category in kanban_data:
        for task in kanban_data[category]:
            task.draw()
    
    if pg.mouse.get_pos()[0] >= screen_width-50:
        image = pg.image.load('images/add.png').convert_alpha()
        image = pg.transform.scale(image, (50,50))
        image_rect = image.get_rect(midright=(screen_width,screen_height/2))
        screen.blit(image, image_rect)

        if pg.mouse.get_pressed()[0] and list(kanban_data)[-1].text != '':
            kanban_data[Category(text='', index=len(kanban_data)+1)] = []
    
    if pg.mouse.get_pos()[1] >= screen_height-50:
        image = pg.image.load('images/add.png').convert_alpha()
        image = pg.transform.scale(image, (50,50))
        image_rect = image.get_rect(midbottom=(screen_width/2,screen_height))
        screen.blit(image, image_rect)

    clock.tick(60)
    pg.display.flip()