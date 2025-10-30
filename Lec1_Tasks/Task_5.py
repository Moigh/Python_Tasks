nums = list(map(int, input().split()))
even_nums = []

for i in nums:
    if i % 2 == 0:
        even_nums.append(str(i))

print(' '.join(even_nums))