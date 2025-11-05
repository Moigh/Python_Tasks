import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шарики")

# Цвета
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = RED
        self.vx = -2
    
    def update(self):
        self.x += self.vx
        
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
    
    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.radius + other.radius:
            self.vx = -self.vx
            other.vx = -other.vx

balls = []

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_ball = Ball(mouse_x, mouse_y)
            balls.append(new_ball)
    
    for ball in balls:
        ball.update()
    
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].check_collision(balls[j])
    
    screen.fill(BLACK)
    
    for ball in balls:
        ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
sys.exit()