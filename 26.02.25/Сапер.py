n, m, k = map(int, input().split())

field = [[0 for _ in range(m)] for _ in range(n)]

mines = []

for _ in range(k):
    row, col = map(int, input().split())
    row -= 1
    col -= 1
    field[row][col] = '*'
    if row + 1 < n:
        if col + 1 < m and field[row+1][col+1] != "*":
            field[row+1][col+1] += 1
        if col - 1 >= 0 and field[row+1][col-1] != "*":
            field[row+1][col-1] += 1
        if field[row+1][col] != "*":
            field[row+1][col] += 1
    if row - 1 >= 0:
        if col + 1 < m and field[row-1][col+1] != "*":
            field[row-1][col+1] += 1
        if col - 1 >= 0 and field[row-1][col-1] != "*":
            field[row-1][col-1] += 1
        if field[row-1][col] != "*":
            field[row-1][col] += 1
    if col + 1 < m and field[row][col+1] != "*":
        field[row][col+1] += 1
    if col - 1 >= 0 and field[row][col-1] != "*":
        field[row][col-1] += 1

for i in range(n):
    # Преобразуем числа в строки и объединяем через пробел
    line = [str(field[i][j]) for j in range(m)]
    print(' '.join(line))