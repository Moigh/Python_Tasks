n = int(input())
line = list(map(int, input().split()))
h = int(input())

for i in range(n):
    if line[i]<h:
        print(i+1)
        break
if line[n-1] >= h:
    print(n+1)
