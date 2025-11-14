import pygame
import os
from .sprites import Snake, Food, Wall
from game.sound import SoundManager


class GameState:
    def __init__(self, width, height, sound_manager):
        self.MARGIN = 22
        self.width = width
        self.height = height
        self.sound_manager = sound_manager

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class MenuScreen(GameState):
    def __init__(self, width, height, sound_manager):
        super().__init__(width, height, sound_manager)
        self.options = ["Free Play", "Level Mode", "Exit"]
        self.selected_index = 0
        self.option_width = 300
        self.option_height = 50

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.sound_manager.play_sound('button')
                if event.key == pygame.K_UP:
                    self.selected_index = (
                        self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (
                        self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_SPACE:
                    if self.selected_index == 0:  # Free Play
                        return FreePlayScreen(
                            self.width, self.height, self.sound_manager)
                    elif self.selected_index == 1:  # Level Mode
                        return LevelScreen(
                            self.width, self.height, self.sound_manager)
                    elif self.selected_index == 2:  # Exit
                        return None
                elif event.key == pygame.K_ESCAPE:
                    return None
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.MARGIN, self.MARGIN, 760, 560), 2)

        font = pygame.font.Font(None, 90)
        title_text = font.render("SNAKE", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(self.width // 2, self.height // 2 - 120))
        screen.blit(title_text, title_rect)

        font = pygame.font.Font(None, 48)
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                0, 0, self.option_width, self.option_height)
            option_rect.center = (
                self.width // 2,
                self.height // 2 - 30 + i * 60)

            if i == self.selected_index:
                pygame.draw.rect(screen, (200, 200, 200), option_rect)
                text_color = (80, 80, 80)
            else:
                text_color = (255, 255, 255)

            option_text = font.render(option, True, text_color)
            text_rect = option_text.get_rect(center=option_rect.center)
            screen.blit(option_text, text_rect)

        font = pygame.font.Font(None, 32)
        instruction_text = font.render(
            "Use ARROWS to navigate, SPACE to select", True, (155, 155, 155))
        instruction_rect = instruction_text.get_rect(
            center=(self.width // 2, self.height // 2 + 200))
        screen.blit(instruction_text, instruction_rect)


class BaseGameScreen(GameState):
    def __init__(self, width, height, sound_manager,
                 mode_name, level_file="level_0.txt"):
        super().__init__(width, height, sound_manager)

        # Константы для игрового поля
        self.TOP_PANEL_Y = self.MARGIN
        self.TOP_PANEL_HEIGHT = 90

        self.CELL_SIZE = 40
        self.CELLS_X, self.CELLS_Y = 19, 11
        self.PANEL_WIDTH = self.CELL_SIZE * self.CELLS_X
        self.GAME_FIELD_Y = self.TOP_PANEL_Y + self.TOP_PANEL_HEIGHT + self.MARGIN
        self.GAME_FIELD_HEIGHT = self.CELLS_Y * self.CELL_SIZE

        self.game_mode = mode_name
        self.score = 0

        # Стены (будут загружены из файла уровня)
        self.walls = []
        self.wall_sprites = pygame.sprite.Group()

        # Загружаем уровень
        self._load_level(level_file)

        # Запускаем музыку
        self.sound_manager.play_background_music()

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

        # Спавним еду с учетом стен и змейки
        self.food.respawn(self.snake.body + self.walls)

        # Таймер для автоматического движения
        self.last_move_time = 0
        self.move_interval = 200
        self.direction_queue = []

        # Флаги для обработки столкновения
        self.game_over = False
        self.collision_timer = 0
        self.collision_delay = 1000

    def _load_level(self, level_file):
        """Загружает уровень из файла"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        filename = os.path.join(project_root, "data", "levels", level_file)

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

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MenuScreen(self.width, self.height,
                                      self.sound_manager)
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
        if self.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.collision_timer > self.collision_delay:
                return GameOverScreen(
                    self.width, self.height, self.sound_manager, self.score)
            return self

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            if self.direction_queue:
                next_dir = self.direction_queue.pop(0)
                self.snake.change_direction(next_dir)

            self.snake.move()
            self.last_move_time = current_time

            # Проверяем ВСЕ типы столкновений
            if self._check_collisions():
                self.sound_manager.stop_background_music()
                self.sound_manager.play_sound('collision')
                self.game_over = True
                self.collision_timer = current_time
            else:
                self._check_food_collision()
                # Проверяем победу (может вернуть новый экран)
                win_screen = self._check_win_condition()
                if win_screen:
                    self.sound_manager.stop_background_music()
                    self.sound_manager.play_sound('victory')
                    return win_screen

        return self

    def _check_collisions(self):
        """Проверяет все типы столкновений"""
        return self._check_self_collision() or self._check_wall_collision()

    def _check_wall_collision(self):
        """Проверяет столкновение со стенами"""
        head_x, head_y = self.snake.body[0]
        return (head_x, head_y) in self.walls

    def _check_self_collision(self):
        """Проверяет столкновение с собой"""
        head_x, head_y = self.snake.body[0]
        for segment_x, segment_y in self.snake.body[1:]:
            if head_x == segment_x and head_y == segment_y:
                return True
        return False

    def _check_food_collision(self):
        """Проверяет столкновение с едой"""
        head_x, head_y = self.snake.body[0]
        food_x, food_y = self.food.position

        if head_x == food_x and head_y == food_y:
            self.score += 1
            self.sound_manager.play_sound('eat')
            self.snake.grow()
            self.food.respawn(self.snake.body + self.walls)

    def _check_win_condition(self):
        """Проверяет условие победы (переопределяется в дочерних классах)"""
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Рисуем стены (если есть)
        self.wall_sprites.draw(screen)

        # Рисуем змейку и яблочко
        self.snake.draw(screen)
        self.food.draw(screen)

        # Рисуем игровое поле
        pygame.draw.rect(
            screen,
            (255,
             255,
             255),
            (self.MARGIN - 2,
             self.GAME_FIELD_Y,
             self.PANEL_WIDTH + 4,
             self.GAME_FIELD_HEIGHT),
            2)

        # Рисуем информацию в верхней панели
        self._draw_ui(screen)

    def _draw_ui(self, screen):
        pygame.draw.rect(
            screen,
            (255,
             255,
             255),
            (self.MARGIN,
             self.TOP_PANEL_Y,
             self.PANEL_WIDTH,
             self.TOP_PANEL_HEIGHT),
            2)
        font = pygame.font.Font(None, 48)

        mode_text = font.render(self.game_mode, True, (255, 255, 255))
        screen.blit(mode_text, (50, 50))

        score_text = font.render(
            f"Score: {
                self.score:03d}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.right = 750
        score_rect.top = 50
        screen.blit(score_text, score_rect)


class GameOverScreen(GameState):
    def __init__(self, width, height, sound_manager, final_score):
        super().__init__(width, height, sound_manager)
        self.final_score = final_score

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return MenuScreen(self.width, self.height,
                                      self.sound_manager)
                elif event.key == pygame.K_ESCAPE:
                    return None
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.MARGIN, self.MARGIN, 760, 560), 2)

        font = pygame.font.Font(None, 72)
        title_text = font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(
            center=(self.width // 2, self.height // 2 - 80))
        screen.blit(title_text, title_rect)

        font = pygame.font.Font(None, 48)
        score_text = font.render(
            f"Final Score: {
                self.final_score:03d}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(self.width // 2, self.height // 2))
        screen.blit(score_text, score_rect)

        font = pygame.font.Font(None, 36)
        restart_text = font.render(
            "Press SPACE for main menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(
            center=(self.width // 2, self.height // 2 + 60))
        screen.blit(restart_text, restart_rect)

        exit_text = font.render("Press ESC to exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(
            center=(self.width // 2, self.height // 2 + 100))
        screen.blit(exit_text, exit_rect)


class FreePlayScreen(BaseGameScreen):
    """Экран свободной игры (уровень без стен)"""

    def __init__(self, width, height, sound_manager):
        super().__init__(width, height, sound_manager, "Free Play", "level_0.txt")

    def _check_win_condition(self):
        """Проверяет условие победы - заполнено все поле"""
        if self.score >= 209:
            return FreePlayVictoryScreen(self.width, self.height, self.score)
        return None


class LevelScreen(BaseGameScreen):
    """Экран игры по уровням"""

    def __init__(self, width, height, sound_manager, level_number=1):
        super().__init__(
            width,
            height,
            sound_manager,
            f"Level {level_number}",
            f"level_{level_number}.txt")
        self.level_number = level_number

    def _check_win_condition(self):
        """Проверяет условие победы - набрано 10 очков"""
        if self.score >= 4:
            return VictoryScreen(
                self.width, self.height, self.sound_manager, self.score, self.level_number)
        return None


class VictoryScreen(GameState):
    def __init__(self, width, height, sound_manager,
                 final_score, level_number=None):
        super().__init__(width, height, sound_manager)
        self.final_score = final_score
        self.level_number = level_number

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Переход на следующий уровень
                    if self.level_number + 1 < 6:
                        next_level = self.level_number + 1
                        return LevelScreen(
                            self.width, self.height, self.sound_manager, next_level)
                    else:
                        return MenuScreen(
                            self.width, self.height, self.sound_manager)
                elif event.key == pygame.K_ESCAPE:
                    return MenuScreen(self.width, self.height,
                                      self.sound_manager)
        return self

    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))

        # Рамка на весь экран
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.MARGIN, self.MARGIN, 760, 560), 2)

        # Заголовок победы
        font = pygame.font.Font(None, 72)
        title_text = font.render("VICTORY!", True, (0, 255, 0))  # Зеленый цвет
        title_rect = title_text.get_rect(
            center=(self.width // 2, self.height // 2 - 100))
        screen.blit(title_text, title_rect)

        # Информация об уровне (если есть)
        font = pygame.font.Font(None, 48)
        if self.level_number:
            level_text = font.render(
                f"Level {
                    self.level_number} Completed", True, (255, 255, 255))
            level_rect = level_text.get_rect(
                center=(self.width // 2, self.height // 2 - 30))
            screen.blit(level_text, level_rect)

        # Инструкция
        font = pygame.font.Font(None, 36)
        continue_text = font.render(
            "Press SPACE to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(
            center=(self.width // 2, self.height // 2 + 80))
        screen.blit(continue_text, continue_rect)

        exit_text = font.render("Press ESC to exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(
            center=(self.width // 2, self.height // 2 + 120))
        screen.blit(exit_text, exit_rect)


class FreePlayVictoryScreen(GameState):
    def __init__(self, width, height, final_score):
        super().__init__(width, height)
        self.final_score = final_score

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Начать заново
                    return FreePlayScreen(
                        self.width, self.height, self.sound_manager)
                elif event.key == pygame.K_ESCAPE:
                    return MenuScreen(self.width, self.height,
                                      self.sound_manager)
        return self

    def draw(self, screen):
        # Черный фон
        screen.fill((0, 0, 0))

        # Рамка на весь экран
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.MARGIN, self.MARGIN, 760, 560), 2)

        # Заголовок победы
        font = pygame.font.Font(None, 72)
        title_text = font.render("YOU WIN!", True, (0, 255, 0))  # Зеленый цвет
        title_rect = title_text.get_rect(
            center=(self.width // 2, self.height // 2 - 80))
        screen.blit(title_text, title_rect)

        # Максимально возможный счет
        max_score = 11 * 19  # 209 очков
        font = pygame.font.Font(None, 48)
        score_text = font.render(
            f"Perfect Score: {
                self.final_score:03d}/{max_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(self.width // 2, self.height // 2))
        screen.blit(score_text, score_rect)

        # Инструкция
        font = pygame.font.Font(None, 36)
        restart_text = font.render(
            "Press SPACE to play again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(
            center=(self.width // 2, self.height // 2 + 60))
        screen.blit(restart_text, restart_rect)

        exit_text = font.render(
            "Press ESC for main menu", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(
            center=(self.width // 2, self.height // 2 + 100))
        screen.blit(exit_text, exit_rect)
