import pygame
from .sprites import Snake, Food

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
        
        # Создаем яблочко
        self.food = Food(
            field_x=self.MARGIN,
            field_y=self.GAME_FIELD_Y,
            cells_x=self.CELLS_X,
            cells_y=self.CELLS_Y,
            cell_size=self.CELL_SIZE
        )
        
        # Таймер для автоматического движения
        self.last_move_time = 0
        self.move_interval = 200  # миллисекунды между движениями (0.2 секунды)
         # Очередь для хранения направлений
        self.direction_queue = []
        
        # Флаги для обработки столкновения
        self.game_over = False
        self.collision_timer = 0
        self.collision_delay = 1000  # 1 секунда задержки перед переходом
    
    def handle_events(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Возвращаемся в меню
                    return MenuScreen(self.width, self.height)
                # Добавляем направление в очередь
                elif event.key == pygame.K_UP:
                    self.direction_queue.append((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.direction_queue.append((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.direction_queue.append((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.direction_queue.append((1, 0))
        return self
    
    def update(self):
        # Если игра уже окончена, ждем перед переходом
        if self.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.collision_timer > self.collision_delay:
                return GameOverScreen(self.width, self.height, self.score)
            return self
        
        # Автоматическое движение змейки по времени
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            # Берем первое направление из очереди (если есть)
            if self.direction_queue:
                next_dir = self.direction_queue.pop(0)  # Берем и удаляем первый элемент
                self.snake.change_direction(next_dir)
            self.snake.move()
            self.last_move_time = current_time
            
            # Проверяем столкновения
            if self._check_self_collision():
                self.game_over = True
                self.collision_timer = current_time
            else:
                self._check_food_collision()
        return self
    
    def _check_food_collision(self):
        # Получаем позицию головы змейки
        head_x, head_y = self.snake.body[0]
        
        # Получаем позицию яблочка
        food_x, food_y = self.food.position
        
        # Если голова змейки на той же клетке, что и яблочко
        if head_x == food_x and head_y == food_y:
            # Увеличиваем счет
            self.score += 1
            # Змейка растет
            self.snake.grow()
            # Яблочко появляется в новом месте
            self.food.respawn()

    def _check_self_collision(self):
        """Проверяет столкновение головы змейки с телом"""
        
        head_x, head_y = self.snake.body[0]
        
        # Проверяем все сегменты кроме головы
        for segment_x, segment_y in self.snake.body[1:]:
            if head_x == segment_x and head_y == segment_y:                
                return True
        
        return False
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рисуем змейку
        self.snake.draw(screen)
        
        # Рисуем яблочко
        self.food.draw(screen)
        
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

class GameOverScreen(GameState):
    def __init__(self, width, height, final_score):
        super().__init__(width, height)
        self.final_score = final_score
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Возвращаемся в главное меню
                    return MenuScreen(self.width, self.height)
                elif event.key == pygame.K_ESCAPE:
                    return None  # Выход из игры
        return self
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рамка на весь экран
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN, self.MARGIN, 760, 560), 2)
        
        # Заголовок
        font = pygame.font.Font(None, 72)
        title_text = font.render("GAME OVER", True, (255, 0, 0))  # Красный цвет
        title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 80))
        screen.blit(title_text, title_rect)
        
        # Итоговый счет
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Final Score: {self.final_score:03d}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        screen.blit(score_text, score_rect)
        
        # Инструкция
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press SPACE for main menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 60))
        screen.blit(restart_text, restart_rect)
        
        exit_text = font.render("Press ESC to exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.width//2, self.height//2 + 100))
        screen.blit(exit_text, exit_rect)