n = input()

even_digits = [1 for digit in n if int(digit) % 2 == 0]
sum = sum(even_digits)
print(sum)