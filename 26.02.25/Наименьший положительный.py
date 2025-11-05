nums = list(map(int, input().split()))

positive_nums = [num for num in nums if num > 0]

min_positive = min(positive_nums)
print(min_positive)