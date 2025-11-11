import pygame
import random

class Snake:
    def __init__(self, field_x, field_y, cells_x, cells_y, cell_size):
        self.field_x = field_x
        self.field_y = field_y
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell_size = cell_size
        
        # Начальная позиция и направление
        start_x = cells_x // 2
        start_y = cells_y // 2
        self.direction = (1, 0)  # Начинаем движение вправо
        
        # Создаем начальное тело змейки (4 сегмента)
        self.body = [
            (start_x, start_y),      # Голова
            (start_x - 1, start_y),  # Тело 1
            (start_x - 2, start_y),  # Тело 2  
            (start_x - 3, start_y)   # Хвост
        ]

         # Флаг роста змейки
        self.grow_pending = False

    def grow(self):
        """Устанавливает флаг роста - змейка увеличится при следующем движении"""
        self.grow_pending = True
    
    def move(self):
        # Получаем текущую позицию головы
        head_x, head_y = self.body[0]
        
        # Вычисляем новую позицию головы
        dir_x, dir_y = self.direction
        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y
        
        # Телепортация через границы
        if new_head_x < 0:
            new_head_x = self.cells_x - 1  # Появляемся справа
        elif new_head_x >= self.cells_x:
            new_head_x = 0  # Появляемся слева
            
        if new_head_y < 0:
            new_head_y = self.cells_y - 1  # Появляемся снизу
        elif new_head_y >= self.cells_y:
            new_head_y = 0  # Появляемся сверху
        
        new_head = (new_head_x, new_head_y)
        
        # Добавляем новую голову в начало
        self.body.insert(0, new_head)
        
        # Удаляем хвост только если не нужно расти
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False  # Сбрасываем флаг роста
    
    def change_direction(self, new_direction):
        # Запрещаем движение в противоположном направлении
        current_dir_x, current_dir_y = self.direction
        new_dir_x, new_dir_y = new_direction
        
        if (new_dir_x != -current_dir_x or new_dir_y != -current_dir_y):
            self.direction = new_direction
    
    def draw(self, screen):
        for segment_x, segment_y in self.body:
            # Вычисляем координаты на экране
            x = self.field_x + segment_x * self.cell_size
            y = self.field_y + segment_y * self.cell_size            
            # Рисуем зеленый квадрат
            pygame.draw.rect(screen, (0, 255, 0), (x, y, self.cell_size, self.cell_size))

class Food:
    def __init__(self, field_x, field_y, cells_x, cells_y, cell_size):
        self.field_x = field_x
        self.field_y = field_y
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell_size = cell_size
        
        # Позиция яблочка в клетках
        self.position = (0, 0)
        
        # Создаем случайную позицию при инициализации
        self.respawn()
    
    def respawn(self):
        """Создает яблочко в случайной позиции на поле"""
        self.position = (
            random.randint(0, self.cells_x - 1),
            random.randint(0, self.cells_y - 1)
        )
    
    def draw(self, screen):
        """Рисует яблочко как красный круг"""
        x = self.field_x + self.position[0] * self.cell_size + self.cell_size // 2
        y = self.field_y + self.position[1] * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2  # Чуть меньше чем клетка
        
        # Рисуем красный круг (яблочко)
        pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)