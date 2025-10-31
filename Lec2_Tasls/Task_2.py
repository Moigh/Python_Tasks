def calc_g(w):
    w = w.upper()
    g = 0
    for c in w:
        g += ord(c) - ord('A') + 1
    return g

words = []
word = input()
while word:
    words.append(word)
    word = input()

sort = sorted(words, key = lambda word: (calc_g(word), word))

for w in sort:
    print(calc_g(w), " ", w)