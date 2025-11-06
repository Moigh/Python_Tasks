numbers = range(10, 100) 
filtered = filter(lambda x: x % 9 == 0, numbers)
squared = map(lambda x: x ** 2, filtered)
result = sum(squared)

print(result)