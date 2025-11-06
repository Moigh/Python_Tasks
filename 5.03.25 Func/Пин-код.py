import math

def check_pin(pinCode):
    parts = pinCode.split('-')
    
    if len(parts) != 3:
        return "Некорректен"
    
    a, b, c = parts
    
    def is_prime(n):
        if not n.isdigit() or int(n) < 2:
            return False
        num = int(n)
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    def is_palindrome(n):
        return n == n[::-1]
    
    def is_power_of_two(n):
        if not n.isdigit() or int(n) < 1:
            return False
        num = int(n)
        return math.log2(num).is_integer()
    
    if is_prime(a) and is_palindrome(b) and is_power_of_two(c):
        return "Корректен"
    else:
        return "Некорректен"

print(check_pin('7-101-4'))
print(check_pin('12-22-16'))