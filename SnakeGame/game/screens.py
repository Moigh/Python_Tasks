import pygame
from .sprites import Snake, Food, Wall

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
    def __init__(self, width, height):
        super().__init__(width, height)
        self.options = ["Free Play", "Level Mode", "Exit"]
        self.selected_index = 0
        self.option_width = 300
        self.option_height = 50
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_SPACE:
                    if self.selected_index == 0:  # Free Play
                        return FreePlayScreen(self.width, self.height)
                    elif self.selected_index == 1:  # Level Mode
                        return LevelScreen(self.width, self.height)
                    elif self.selected_index == 2:  # Exit
                        return None
                elif event.key == pygame.K_ESCAPE:
                    return None
        return self
    
    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рамка на весь экран
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN, self.MARGIN, 760, 560), 2)
        
        # Заголовок игры
        font = pygame.font.Font(None, 90)
        title_text = font.render("SNAKE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 120))
        screen.blit(title_text, title_rect)
        
        # Опции меню
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(self.options):
            # Позиция для опции
            option_rect = pygame.Rect(0, 0, self.option_width, self.option_height)
            option_rect.center = (self.width//2, self.height//2 - 30 + i * 60)
            
            # Рисуем прямоугольник для выбранной опции
            if i == self.selected_index:
                pygame.draw.rect(screen, (200, 200, 200), option_rect)  # Светло-серый фон
                text_color = (80, 80, 80)  # Темно-серый текст
            else:
                text_color = (255, 255, 255)  # Белый текст
            
            # Рисуем текст опции
            option_text = font.render(option, True, text_color)
            text_rect = option_text.get_rect(center=option_rect.center)
            screen.blit(option_text, text_rect)
        
        # Инструкция
        font = pygame.font.Font(None, 32)
        instruction_text = font.render("Use ARROWS to navigate, SPACE to select", True, (155, 155, 155))
        instruction_rect = instruction_text.get_rect(center=(self.width//2, self.height//2 + 200))
        screen.blit(instruction_text, instruction_rect)

class BaseGameScreen(GameState):
    def __init__(self, width, height, mode_name):
        super().__init__(width, height)
        
        # Константы для игрового поля
        self.TOP_PANEL_Y = self.MARGIN
        self.TOP_PANEL_HEIGHT = 90
        
        self.CELL_SIZE = 40
        self.CELLS_X, self.CELLS_Y = 19, 11
        self.PANEL_WIDTH = self.CELL_SIZE * self.CELLS_X
        self.GAME_FIELD_Y = self.TOP_PANEL_Y + self.TOP_PANEL_HEIGHT + self.MARGIN
        self.GAME_FIELD_HEIGHT = self.CELLS_Y * self.CELL_SIZE
        
        self.game_mode = mode_name
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
        
        self.food.respawn(self.snake.body)
        
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
                self._check_win_condition()  # Проверка победы
        return self
        
    def _check_win_condition(self):
        """Проверяет условие победы (переопределяется в дочерних классах)"""
        pass
    
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
            self.food.respawn(self.snake.body)

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
        mode_text = font.render(self.game_mode, True, (255, 255, 255))
        screen.blit(mode_text, (50, 50))
        
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

class FreePlayScreen(BaseGameScreen):
    """Экран свободной игры"""
    def __init__(self, width, height):
        super().__init__(width, height, "Free Play")

class LevelScreen(BaseGameScreen):
    """Экран игры по уровням"""
    def __init__(self, width, height, level_number=1):
        self.level_number = level_number
        self.walls = []  # Список позиций стен
        self.wall_sprites = pygame.sprite.Group()
        super().__init__(width, height, f"Level {level_number}")
        self._load_level(level_number)
        self.food.respawn(self.snake.body + self.walls)
        
    def _load_level(self, level_number):
        """Загружает уровень из файла"""
        import os
        
        # Получаем абсолютный путь к файлу уровня
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        project_root = os.path.dirname(current_dir)
        filename = os.path.join(project_root, "data", "levels", f"level_{level_number}.txt")

        """Загружает уровень из файла"""
        with open(filename, 'r') as file:
            level_data = [line.strip() for line in file]
        
        # Очищаем предыдущие стены
        self.walls = []
        self.wall_sprites.empty()
        
        # Парсим уровень
        for y, row in enumerate(level_data):
            for x, cell in enumerate(row):
                if cell == '#':  # Стена
                    self.walls.append((x, y))
                    wall = Wall(
                        self.MARGIN, self.GAME_FIELD_Y,
                        x, y, self.CELL_SIZE,
                        self.wall_sprites
                    )
        
    def _check_collisions(self):
        """Проверяет столкновения со стенами и с собой"""
        return self._check_wall_collision() or self._check_self_collision()

    def _check_wall_collision(self):
        """Проверяет столкновение головы змейки со стенами"""
        head_x, head_y = self.snake.body[0]
        return (head_x, head_y) in self.walls

    def _check_food_collision(self):
        head_x, head_y = self.snake.body[0]
        food_x, food_y = self.food.position
        
        if head_x == food_x and head_y == food_y:
            self.score += 1
            self.snake.grow()
            # Учитываем стены при респавне яблочка
            self.food.respawn(self.snake.body + self.walls)

    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))
        
        # Рисуем стены
        self.wall_sprites.draw(screen)
        
        # Рисуем змейку и яблочко
        self.snake.draw(screen)
        self.food.draw(screen)
        
        # Рисуем игровое поле
        pygame.draw.rect(screen, (255, 255, 255), (self.MARGIN - 2, self.GAME_FIELD_Y, self.PANEL_WIDTH + 4, self.GAME_FIELD_HEIGHT), 2)
        
        # Рисуем информацию в верхней панели
        self._draw_ui(screen)