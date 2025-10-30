n = int(input())
f = [1, 1]

for i in range(2, n):
    num = f[i-1] + f[i-2]
    f.append(num)

print(' '.join(map(str, f[:n])))