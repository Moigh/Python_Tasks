import pygame
import random

pygame.init()

BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.opened = [[False] * width for _ in range(height)]
        self.mines_count = 10
        
        self.place_mines()
        
        self.left = 10
        self.top = 10 
        self.cell_size = 30

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != 10:
                self.board[y][x] = 10
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != 10:
                            self.board[ny][nx] += 1
                mines_placed += 1
                self.opened[y][x] = True 
        
    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (self.left <= x < self.left + self.width * self.cell_size and
            self.top <= y < self.top + self.height * self.cell_size):
            cell_x = (x - self.left) // self.cell_size
            cell_y = (y - self.top) // self.cell_size
            return (cell_x, cell_y)
        return None
    
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            x, y = cell
            self.opened[y][x] = True
    
    def render(self, screen):
        font = pygame.font.Font(None, 24)
        
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size, self.cell_size
                )
                
                pygame.draw.rect(screen, WHITE, rect, 1)
                
                if self.opened[y][x]:
                    if self.board[y][x] == 10:
                        pygame.draw.rect(screen, RED, rect.inflate(-4, -4))
                    else:
                        text = font.render(str(self.board[y][x]), True, WHITE)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)

screen = pygame.display.set_mode((320, 320))
board = Board(10, 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)
    
    screen.fill(BLACK)
    board.render(screen)
    pygame.display.flip()

pygame.quit()