n = input()

sum = 0

for i in n:
    num = int(i)
    if num % 2 == 0:
        sum += 1

print(sum)