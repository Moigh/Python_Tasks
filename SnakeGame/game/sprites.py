import pygame
import random
import os

def load_image(name):
    """Загружает изображение из папки assets/snake_parts"""
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    fullname = os.path.join(project_root, "assets", "snake_parts", name)
    
    if not os.path.isfile(fullname):
        print(f"Предупреждение: файл {fullname} не найден!")
        surf = pygame.Surface((40, 40))
        surf.fill((255, 0, 0) if "food" in name else (0, 255, 0))
        return surf
    
    image = pygame.image.load(fullname)
    return image.convert_alpha()

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, segment_type, direction1, direction2, pos_x, pos_y, field_x, field_y, cell_size):
        super().__init__()
        
        # Загружаем нужную картинку
        if segment_type == 'head':
            self.base_image = load_image("head.png")
            direction = direction1
        elif segment_type == 'body':
            self.base_image = load_image("body.png")
            direction = direction1
        elif segment_type == 'tail':
            self.base_image = load_image("tail.png")
            direction = direction1
        elif segment_type == 'turn':
            self.base_image = load_image("turn.png")
            # Для поворота определяем правильное направление на основе двух направлений
            direction = self._get_turn_direction(direction1, direction2)
        
        # Поворачиваем картинку
        self.image = self._rotate_image(self.base_image, direction)
        self.rect = self.image.get_rect()
        self.rect.x = field_x + pos_x * cell_size
        self.rect.y = field_y + pos_y * cell_size
    
    def _get_turn_direction(self, in_dir, out_dir):
        """Определяет правильное направление для поворота"""
        # Комбинации поворотов и их направления
        turns = {
            # Повороты направо (по часовой)
            ((0, -1), (1, 0)): (0, -1),   # Вверх -> Вправо
            ((1, 0), (0, 1)): (1, 0),     # Вправо -> Вниз
            ((0, 1), (-1, 0)): (0, 1),    # Вниз -> Влево
            ((-1, 0), (0, -1)): (-1, 0),  # Влево -> Вверх
            
            # Повороты налево (против часовой)
            ((0, -1), (-1, 0)): (-1, 0),  # Вверх -> Влево
            ((-1, 0), (0, 1)): (0, 1),    # Влево -> Вниз
            ((0, 1), (1, 0)): (1, 0),     # Вниз -> Вправо
            ((1, 0), (0, -1)): (0, -1),   # Вправо -> Вверх
        }
        
        return turns.get((in_dir, out_dir), in_dir)
    
    def _rotate_image(self, image, direction):
        """Поворачивает картинку согласно направлению"""
        if direction == (0, -1):  # Вверх
            return image
        elif direction == (1, 0):  # Вправо
            return pygame.transform.rotate(image, -90)
        elif direction == (0, 1):  # Вниз
            return pygame.transform.rotate(image, 180)
        elif direction == (-1, 0):  # Влево
            return pygame.transform.rotate(image, 90)
        return image

class Snake:
    def __init__(self, field_x, field_y, cells_x, cells_y, cell_size):
        self.field_x = field_x
        self.field_y = field_y
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell_size = cell_size
        
        start_x = cells_x // 2
        start_y = cells_y // 2
        self.direction = (1, 0)  # Начинаем движение вправо
        
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
            (start_x - 3, start_y)
        ]
        
        self.segments = pygame.sprite.Group()
        self._create_segments()
        self.grow_pending = False

    def _create_segments(self):
        """Создает спрайты для змейки"""
        self.segments.empty()
        
        for i, (pos_x, pos_y) in enumerate(self.body):
            if i == 0:  # Голова
                segment_type = 'head'
                direction = self.direction
                # Для головы передаем только одно направление
                segment = SnakeSegment(segment_type, direction, None, pos_x, pos_y,
                                    self.field_x, self.field_y, self.cell_size)
                
            elif i == len(self.body) - 1:  # Хвост
                segment_type = 'tail'
                prev_pos = self.body[i-1]
                # Направление хвоста - куда он смотрит
                direction = (pos_x - prev_pos[0], pos_y - prev_pos[1])
                # Для хвоста передаем только одно направление
                segment = SnakeSegment(segment_type, direction, None, pos_x, pos_y,
                                    self.field_x, self.field_y, self.cell_size)
                
            else:  # Тело
                prev_pos = self.body[i-1]
                next_pos = self.body[i+1]
                
                to_prev = (prev_pos[0] - pos_x, prev_pos[1] - pos_y)
                to_next = (next_pos[0] - pos_x, next_pos[1] - pos_y)
                
                # Если это прямая линия - это тело
                if to_prev[0] == -to_next[0] and to_prev[1] == -to_next[1]:
                    segment_type = 'body'
                    direction = to_prev
                    segment = SnakeSegment(segment_type, direction, None, pos_x, pos_y,
                                        self.field_x, self.field_y, self.cell_size)
                else:
                    # Если это угол - это поворот, передаем ОБА направления
                    segment_type = 'turn'
                    segment = SnakeSegment(segment_type, to_prev, to_next, pos_x, pos_y,
                                        self.field_x, self.field_y, self.cell_size)
            
            self.segments.add(segment)

    def grow(self):
        self.grow_pending = True
    
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y
        
        # Телепортация через границы
        if new_head_x < 0: new_head_x = self.cells_x - 1
        elif new_head_x >= self.cells_x: new_head_x = 0
        if new_head_y < 0: new_head_y = self.cells_y - 1  
        elif new_head_y >= self.cells_y: new_head_y = 0
        
        self.body.insert(0, (new_head_x, new_head_y))
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
        
        self._create_segments()
    
    def change_direction(self, new_direction):
        current_dir_x, current_dir_y = self.direction
        new_dir_x, new_dir_y = new_direction
        if (new_dir_x != -current_dir_x or new_dir_y != -current_dir_y):
            self.direction = new_direction
    
    def draw(self, screen):
        self.segments.draw(screen)

class Food(pygame.sprite.Sprite):
    def __init__(self, field_x, field_y, cells_x, cells_y, cell_size):
        super().__init__()
        self.field_x = field_x
        self.field_y = field_y
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell_size = cell_size
        
        # Загружаем изображение еды
        self.image = load_image("food.png")
        self.rect = self.image.get_rect()
        
        # Позиция яблочка в клетках
        self.position = (0, 0)
    
    def respawn(self, snake_body):
        """Создает яблочко в случайной позиции, не занятой змейкой"""
        max_attempts = 100
        
        for attempt in range(max_attempts):
            new_position = (
                random.randint(0, self.cells_x - 1),
                random.randint(0, self.cells_y - 1)
            )
            
            if new_position not in snake_body:
                self.position = new_position
                self.rect.x = self.field_x + new_position[0] * self.cell_size
                self.rect.y = self.field_y + new_position[1] * self.cell_size
                return
        
        # Если не нашли свободную клетку
        for x in range(self.cells_x):
            for y in range(self.cells_y):
                if (x, y) not in snake_body:
                    self.position = (x, y)
                    self.rect.x = self.field_x + x * self.cell_size
                    self.rect.y = self.field_y + y * self.cell_size
                    return
    
    def draw(self, screen):
        """Рисует яблочко (теперь через спрайт)"""
        screen.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, field_x, field_y, cell_x, cell_y, cell_size, *groups):
        super().__init__(*groups)
        self.field_x = field_x
        self.field_y = field_y
        self.cell_size = cell_size
        
        # Создаем поверхность для стены
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill((100, 100, 100))  # Серый цвет для стен
        
        self.rect = self.image.get_rect()
        self.rect.x = field_x + cell_x * cell_size
        self.rect.y = field_y + cell_y * cell_size