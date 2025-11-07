class Summator:
    def transform(self, n):
        return n
    
    def sum(self, N):
        total = 0
        for n in range(1, N + 1):
            total += self.transform(n)
        return total

class SquareSummator(Summator):
    def transform(self, n):
        return n ** 2

class CubeSummator(Summator):
    def transform(self, n):
        return n ** 3


# Проверка

summator = Summator()
N = 10
expected = N * (N + 1) / 2
if summator.sum(N) == expected:
    print("Пройдено")

square_summator = SquareSummator()
expected_squares = N * (N + 1) * (2 * N + 1) / 6
if square_summator.sum(N) == expected_squares:
    print("Пройдено")

cube_summator = CubeSummator()
expected_cubes = (N * (N + 1) / 2) ** 2
if cube_summator.sum(N) == expected_cubes:
    print("Пройдено")
