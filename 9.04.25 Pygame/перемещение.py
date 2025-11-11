import pygame as pg

pg.init()

screen = pg.display.set_mode((300, 300))

square_size = 50
square_color = (255, 0, 0) 
square_x, square_y = 0, 0

dragging = False
d_x, d_y = 0, 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if (square_x <= mouse_x <= square_x + square_size and 
                    square_y <= mouse_y <= square_y + square_size):
                    dragging = True
                    d_x = mouse_x - square_x
                    d_y = mouse_y - square_y        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False        
        if event.type == pg.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                square_x = mouse_x - d_x
                square_y = mouse_y - d_y                
                square_x = max(0, min(square_x, 300 - square_size))
                square_y = max(0, min(square_y, 300 - square_size))    
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))    
    pg.display.flip()
pg.quit()