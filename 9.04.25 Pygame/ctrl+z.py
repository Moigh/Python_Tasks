import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

screen2 = pygame.Surface(screen.get_size())
x1, y1, w, h = 0, 0, 0, 0
drawing = False

rectangles_history = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x1, y1 = event.pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            if w != 0 and h != 0:
                rect_data = (min(x1, x1 + w), min(y1, y1 + h), abs(w), abs(h))
                rectangles_history.append(rect_data)
            w, h = 0, 0
            drawing = False
        
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                w, h = event.pos[0] - x1, event.pos[1] - y1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                if rectangles_history:
                    rectangles_history.pop()
    
    screen.fill(pygame.Color('black'))
    screen.blit(screen2, (0, 0))
    
    for rect in rectangles_history:
        pygame.draw.rect(screen, (0, 0, 255), rect, 5)
    
    if drawing:
        x = min(x1, x1 + w)
        y = min(y1, y1 + h)
        width = abs(w)
        height = abs(h)
        pygame.draw.rect(screen, (0, 0, 255), (x, y, width, height), 5)
    
    pygame.display.flip()

pygame.quit()
sys.exit()