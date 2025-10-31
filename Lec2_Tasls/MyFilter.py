def my_filter(func, arr):
    res = []
    for i in arr:
        if func(i):
            res.append(i)
    return res

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_nums = my_filter(lambda x: x % 2 == 0, nums)
print(even_nums)