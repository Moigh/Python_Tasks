import pygame
import sys

pygame.init()

TILE_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 8
SCREEN_SIZE = (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Ящики")

grass_img = pygame.image.load("./7.05.25 Pygame 2/grass.jpeg").convert()
box_img = pygame.image.load("./7.05.25 Pygame 2/box.png").convert()
player_img = pygame.image.load("./7.05.25 Pygame 2/boy.png").convert_alpha()

# 0 - трава, 1 - ящик
level = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

player_x, player_y = 1, 1
player_dir = (1, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                player_dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                player_dir = (0, 1)
            elif event.key == pygame.K_LEFT:
                player_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                player_dir = (1, 0)
            
            if event.key == pygame.K_SPACE:
                target_x = player_x + player_dir[0]
                target_y = player_y + player_dir[1]
                if (0 <= target_x < GRID_WIDTH and 0 <= target_y < GRID_HEIGHT and 
                    level[target_y][target_x] == 1):
                    level[target_y][target_x] = 0
            elif (0 <= player_x+player_dir[0] < GRID_WIDTH and 0 <= player_y+player_dir[1] < GRID_HEIGHT and 
                level[player_y+player_dir[1]][player_x+player_dir[0]] == 0):
                player_x, player_y = player_x+player_dir[0], player_y+player_dir[1]
            
    
    screen.fill((0, 0, 0))
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            if level[y][x] == 0:
                screen.blit(grass_img, pos)
            else:
                screen.blit(box_img, pos)
    
    player_pos = (player_x * TILE_SIZE, player_y * TILE_SIZE)
    screen.blit(player_img, player_pos)
    
    pygame.display.flip()

pygame.quit()
sys.exit()