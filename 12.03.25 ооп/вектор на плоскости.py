class MyVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return MyVector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return MyVector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return MyVector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar  
        return self
    
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return f"MyVector({self.x}, {self.y})"

# Пример 1
v1 = MyVector(-2, 5)
v2 = MyVector(3, -4)
v_sum = v1 + v2
print(v_sum) 