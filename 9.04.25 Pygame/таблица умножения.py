import pygame
import math
from math import cos, sin, radians

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RADIUS = 200
NUM_POINTS = 360
center_x, center_y = WIDTH // 2, HEIGHT // 2 

multiplier = 2.0
multiplier_speed = 0.01
paused = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    
    if not paused:
        multiplier += multiplier_speed
    
    screen.fill(BLACK)
    
    pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), RADIUS, 1)
    
    for i in range(NUM_POINTS):
        x1 = int(cos(radians(i)) * RADIUS) + center_x
        y1 = int(sin(radians(i)) * RADIUS) + center_y
        
        x2 = int(cos(radians((i * multiplier) % NUM_POINTS)) * RADIUS) + center_x
        y2 = int(sin(radians((i * multiplier) % NUM_POINTS)) * RADIUS) + center_y
        
        import colorsys
        hue = i / NUM_POINTS
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 1)
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"{multiplier:.2f}", True, WHITE)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()