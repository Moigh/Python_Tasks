import pygame as pg

pg.init()

while True:
    W, N = map(int, input("Введите W и N: ").split())

    if W % N != 0:
        print("Ошибка: W должно быть кратно N")
    else:
        break

screen = pg.display.set_mode((W, W))

cell_size = W // N

for row in range(N):
    for col in range(N):
        if (row + col) % 2 == 0:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255) 
        
        pg.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

pg.display.flip()

while pg.event.wait().type != pg.QUIT:
    pass

pg.quit()