import pygame
from .sprites import Snake

class GameState:
    def __init__(self, width, height):
        self.MARGIN = 22
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
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN, self.MARGIN, 760, 560), 2)
        
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
        self.TOP_PANEL_Y = self.MARGIN
        self.TOP_PANEL_HEIGHT = 90
        
        self.CELL_SIZE = 40
        self.CELLS_X, self.CELLS_Y = 19, 11
        self.PANEL_WIDTH = self.CELL_SIZE * self.CELLS_X
        self.GAME_FIELD_Y = self.TOP_PANEL_Y + self.TOP_PANEL_HEIGHT + self.MARGIN
        self.GAME_FIELD_HEIGHT = self.CELLS_Y * self.CELL_SIZE
        
        self.level = 1
        self.score = 0
        
        # Создаем змейку
        self.snake = Snake(
            field_x=self.MARGIN,
            field_y=self.GAME_FIELD_Y,
            cells_x=self.CELLS_X,
            cells_y=self.CELLS_Y,
            cell_size=self.CELL_SIZE
        )
        
        # Таймер для автоматического движения
        self.last_move_time = 0
        self.move_interval = 200  # миллисекунды между движениями (0.2 секунды)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Возвращаемся в меню
                    return MenuScreen(self.width, self.height)
                # Управление змейкой - только меняем направление
                elif event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
        return self
    
    def update(self):
        # Автоматическое движение змейки по времени
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            self.snake.move()
            self.last_move_time = current_time
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рисуем змейку
        self.snake.draw(screen)
        
        # Рисуем игровое поле
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN - 2, self.GAME_FIELD_Y, self.PANEL_WIDTH + 4, self.GAME_FIELD_HEIGHT), 2)
        
        # Рисуем информацию в верхней панели
        self._draw_ui(screen)
    
    def _draw_ui(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN, self.TOP_PANEL_Y, self.PANEL_WIDTH, self.TOP_PANEL_HEIGHT), 2)
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