n = int(input())
lat_eng = {}

for _ in range(n):
    eng, latins = input().split(' - ')
    lat_words = [word.strip() for word in latins.split(',')]
    for lat in lat_words:
        lat_eng.setdefault(lat, []).append(eng)

print(len(lat_eng))
for lat in sorted(lat_eng):
    print(f"{lat} - {', '.join(sorted(lat_eng[lat]))}")