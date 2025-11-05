import sys

words = sys.stdin.read().split()

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) - 1

word_freq = [(count, word) for word, count in freq.items()]

word_freq.sort()

for count, word in word_freq:
    print(word)