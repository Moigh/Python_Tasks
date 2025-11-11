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
                    # Переходим к игровому экрану
                    return GameScreen(self.width, self.height)
                elif event.key == pygame.K_ESCAPE:
                    return None  # Выход из игры
        return self
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рамка на весь экран
        pygame.draw.rect(screen, (255, 255, 255), (20, 20, 760, 560), 2)
        
        # Заголовок игры
        font = pygame.font.Font(None, 72)
        title_text = font.render("SNAKE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 50))
        screen.blit(title_text, title_rect)
        
        # Инструкция
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.width//2, self.height//2 + 50))
        screen.blit(start_text, start_rect)
        
        exit_text = font.render("Press ESC to exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.width//2, self.height//2 + 100))
        screen.blit(exit_text, exit_rect)

class GameScreen(GameState):
    def __init__(self, width, height):
        super().__init__(width, height)
        
        # Константы для игрового поля
        self.MARGIN = 20
        self.TOP_PANEL_Y = 25
        self.TOP_PANEL_HEIGHT = 90
        self.GAME_FIELD_Y = self.TOP_PANEL_Y + self.TOP_PANEL_HEIGHT + self.MARGIN  # 25 + 90 + 20 = 135
        
        self.PANEL_WIDTH = 760
        self.CELL_SIZE = 40  # 760 / 19 = 40
        self.CELLS_X, self.CELLS_Y = 19, 11
        self.GAME_FIELD_HEIGHT = self.CELLS_Y * self.CELL_SIZE  # 11 * 40 = 440
        
        self.level = 1
        self.score = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Возвращаемся в меню
                    return MenuScreen(self.width, self.height)
        return self
    
    def update(self):
        # Пока ничего не обновляем
        pass
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рисуем сетку игрового поля
        self._draw_grid(screen)
        
        # Рисуем информацию в верхней панели
        self._draw_ui(screen)
    
    def _draw_grid(self, screen):
        # Вертикальные линии
        for x in range(self.CELLS_X + 1):
            pygame.draw.line(
                screen, (255, 255, 255),
                (self.MARGIN + x * self.CELL_SIZE, self.GAME_FIELD_Y),
                (self.MARGIN + x * self.CELL_SIZE, self.GAME_FIELD_Y + self.GAME_FIELD_HEIGHT),
                2
            )
        
        # Горизонтальные линии
        for y in range(self.CELLS_Y + 1):
            pygame.draw.line(
                screen, (255, 255, 255),
                (self.MARGIN, self.GAME_FIELD_Y + y * self.CELL_SIZE),
                (self.MARGIN + self.PANEL_WIDTH, self.GAME_FIELD_Y + y * self.CELL_SIZE),
                2
            )
    
    def _draw_ui(self, screen):
        """Рисует интерфейс в верхней панели"""
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN, self.TOP_PANEL_Y, self.PANEL_WIDTH, self.TOP_PANEL_HEIGHT), 2)  # Верхняя панель
        font = pygame.font.Font(None, 48)
        
        # Уровень слева
        level_text = font.render(f"LVL. {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (50, 50))
        
        # Счет справа (3 цифры)
        score_text = font.render(f"Score: {self.score:03d}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.right = 750
        score_rect.top = 50
        screen.blit(score_text, score_rect)