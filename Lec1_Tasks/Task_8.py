n, k = map(int, input().split())

pins = ['I'] * n

for j in range(k):
    l, r = map(int, input().split())
    l -= 1
    for i in range(l, r):
        pins[i] = '.'

print(''.join(pins))