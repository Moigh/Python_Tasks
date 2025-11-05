city_to_country = {}
n = int(input())
output = []

for _ in range(n):
    data = input().split()
    country = data[0]
    cities = data[1:]

    for city in cities:
        city_to_country[city] = country

m = int(input())

for _ in range(m):
    city = input().strip()
    output.append(city_to_country[city])
print('\n'.join(output))