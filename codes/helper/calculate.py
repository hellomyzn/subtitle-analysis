import collections


def count_words(words_without_noises):
    c = collections.Counter(words_without_noises)
    return c.most_common()


def count_words_by_frequency(frequency, words):
    words_by_frequency = {}

    for i in range(1, frequency + 1):
        for word, times in words:
            if frequency <= times:
                words_by_frequency.setdefault(str(frequency), []).append(word)
            elif times == i: 
                words_by_frequency.setdefault(str(i), []).append(word)

    return words_by_frequency