import pygame

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
    
    def move(self):
        """Двигает змейку в текущем направлении"""
        # Получаем текущую позицию головы
        head_x, head_y = self.body[0]
        
        # Вычисляем новую позицию головы
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Добавляем новую голову в начало
        self.body.insert(0, new_head)
        
        # Удаляем последний сегмент (хвост)
        self.body.pop()
    
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