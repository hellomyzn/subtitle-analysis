import collections


def count_words(words_without_noises):
    c = collections.Counter(words_without_noises)
    return c.most_common()


def count_words_by_frequency(frequency, words):
    words_by_frequency = {}

    for i in range(1, frequency + 1):
        for word, times in words:
            if frequency <= times and frequency == i:
                words_by_frequency.setdefault(str(frequency), []).append([word, times])
            elif times == i: 
                words_by_frequency.setdefault(str(i), []).append([word,times])

    return words_by_frequency


def percentage_of_words(all_word_times: int, words: int):
    percentage = round((words / all_word_times) * 100, 1)
    return percentage
