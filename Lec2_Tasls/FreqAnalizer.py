def get_word_frequency(text):
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# Использование
text = input()
freq_dict = get_word_frequency(text)
print(freq_dict)