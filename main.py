import pygame as pg

pg.init()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
clock = pg.time.Clock()
title_font_size = 40
text_font_size = 20
title_font = pg.font.SysFont('chalkduster', title_font_size)
text_font = pg.font.SysFont('chalkduster', text_font_size)
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
        self.editing = False
    
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

        if self.editing and int(pg.time.get_ticks() / 1000) % 2 == 0:
            caret_x = surface.get_rect().right - text_font_size
            caret_y = surface.get_rect().bottom - text_font_size

            pg.draw.line(surface, (255,255,255), (caret_x,caret_y), (caret_x,caret_y-text_font_size))
        
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


def find_task_text(text):
    for category in kanban_data:
        for task in kanban_data[category]:
            if task.text == text:
                return True
    
    return False


def draw_add_symbol(position, x_pos, y_pos):
    image = pg.image.load('images/add.png').convert_alpha()
    image = pg.transform.scale(image, (50,50))
    if position == 'midright':
        image_rect = image.get_rect(midright=(x_pos, y_pos))
    elif position == 'midbottom':
        image_rect = image.get_rect(midbottom=(x_pos, y_pos))
    screen.blit(image, image_rect)


def get_category_from_mouse_position():
    section_distances = get_section_distances()

    index = 0
    x_val = 0
    while x_val < pg.mouse.get_pos()[0]:
        x_val += section_distances
        index += 1
    
    category = list(kanban_data)[index-1]
    
    return category


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


section_names = ['to do', 'in progress', 'done']
'''new_name = ' '
while new_name != '':
    new_name = input('type category name or leave blank to finish: ')
    section_names.append(new_name)'''

kanban_data = {}

for index, name in enumerate(section_names):
    kanban_data[Category(text=name, index=index+1)] = []

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
                        selected.editing = not selected.editing
                        break
                    
        if event.type == pg.MOUSEBUTTONUP and selected != None:
            category = get_category_from_mouse_position()

            selected.background_colour = (100,100,100)
            selected.category.tasks.remove(selected)
            category.tasks.append(selected)
            selected.category = category
            selected = None
        
        if event.type == pg.KEYUP:
            for category in kanban_data:
                for task in kanban_data[category]:
                    if task.editing:
                        if event.key in (pg.K_a, pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f, pg.K_g, pg.K_h, pg.K_i, pg.K_j, pg.K_k, pg.K_l, pg.K_m, pg.K_n, pg.K_o, pg.K_p, pg.K_q, pg.K_r, pg.K_s, pg.K_t, pg.K_u, pg.K_v, pg.K_w, pg.K_x, pg.K_y, pg.K_z, pg.K_SPACE):
                            task.text += event.unicode
                        elif event.key == pg.K_BACKSPACE:
                            task.text = task.text[:-1]
                        elif event.key == pg.K_RETURN:
                            task.editing = False
    
    # draw everything
    title_text_surfaces = draw_section_titles()
    draw_vertical_borders()
    draw_horizontal_border(title_text_surfaces)
    for category in kanban_data:
        for task in kanban_data[category]:
            task.draw()
    
    # add new task
    if pg.mouse.get_pos()[1] >= screen_height-50:
        category = get_category_from_mouse_position()
            
        x_pos = category.index * get_section_distances()
        x_pos -= get_section_distances() // 2
        
        draw_add_symbol('midbottom', x_pos, screen_height)

        if pg.mouse.get_pressed()[0] and find_task_text('') == False:
            create_task('', category)
            

    clock.tick(60)
    pg.display.flip()
