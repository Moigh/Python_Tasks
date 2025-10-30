n = int(input())
arr = list(map(int, input().split()))
k = int(input())
k = k % n
if k < 0:
    k = n + k

if k != 0:
    arr[:] = arr[::-1]
    arr[:k] = arr[:k][::-1]
    arr[k:] = arr[k:][::-1]
print(' '.join(map(str, arr)))