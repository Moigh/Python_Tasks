class Queue:
    def __init__(self, *values):
        self._items = list(values)
    
    def append(self, *values):
        if not values:
            return
        self._items.extend(values)
    
    def copy(self):
        return Queue(*self._items)
    
    def pop(self):
        if not self._items:
            return None
        return self._items.pop(0)
    
    def extend(self, queue):
        self._items.extend(queue._items)
    
    def next(self):
        if len(self._items) <= 1:
            return Queue()
        return Queue(*self._items[1:])
    
    def __add__(self, other):
        return Queue(*(self._items + other._items))
    
    def __iadd__(self, other):
        self.extend(other)
        return self
    
    def __eq__(self, other):
        return self._items == other._items
    
    def __rshift__(self, n):
        if n >= len(self._items):
            return Queue()
        return Queue(*self._items[n:])
    
    def __str__(self):
        if not self._items:
            return "[]"
        return "[" + " -> ".join(map(str, self._items)) + "]"
    
    def __iter__(self):
        return iter(self._items)


q1 = Queue(1, 2, 3)
print(q1) 

q1.append(4, 5)
print(q1) 

qx = q1.copy()
print(qx.pop()) 
print(qx)  

q2 = q1.copy()
print(q2) 
print(q1 == q2, id(q1) == id(q2))

q3 = q2.next()
print(q1, q2, q3, sep='\n')  

print(q1 + q3)  

