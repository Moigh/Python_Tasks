nums = list(map(int, input().split()))
min = 1001

for num in nums:
    if num > 0 and num < min:
        min = num
print(min)