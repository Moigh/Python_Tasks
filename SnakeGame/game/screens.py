import pygame

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def handle_events(self, events):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass

class MenuScreen(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Начало игры!")  # Пока просто выводим в консоль
                    return self  # Остаемся в меню
                elif event.key == pygame.K_ESCAPE:
                    return None  # Выход из игры
        return self
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рамка поля (белый контур)
        pygame.draw.rect(screen, (255, 255, 255), (21, 25, 762, 544), 2)  # Игровое поле
        
        # Заголовок игры
        font = pygame.font.Font(None, 72)
        title_text = font.render("SNAKE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 50))
        screen.blit(title_text, title_rect)
        
        # Инструкция
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to start", True, (125, 125, 125))
        start_rect = start_text.get_rect(center=(self.width//2, self.height//2 + 50))
        screen.blit(start_text, start_rect)
        
        exit_text = font.render("Press ESC to exit", True, (125, 125, 125))
        exit_rect = exit_text.get_rect(center=(self.width//2, self.height//2 + 100))
        screen.blit(exit_text, exit_rect)