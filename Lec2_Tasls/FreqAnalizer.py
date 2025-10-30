def freq_analizer(text):
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

text = input()
freq_dict = freq_analizer(text)
print(freq_dict)