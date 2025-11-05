nums = map(int, input().split())
even_nums = map(str, filter(lambda x: x % 2 == 0, nums))

print(' '.join(even_nums))