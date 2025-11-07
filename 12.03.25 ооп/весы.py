class Balance:
    def __init__(self):
        self.left = 0
        self.right = 0
    
    def add_right(self, w):
        self.right += w
    
    def add_left(self, w):
        self.left += w
    
    def result(self):
        if self.left == self.right:
            return '='
        elif self.left > self.right:
            return 'L' 
        else:
            return'R'
        
# Пример 1
balance = Balance()
balance.add_right(10)
balance.add_left(9)
balance.add_left(2)
print(balance.result())

# Пример 2
balance = Balance()
balance.add_right(10)
balance.add_left(5)
balance.add_left(5)
print(balance.result())
balance.add_left(1)
print(balance.result())