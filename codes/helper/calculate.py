import collections


def count_words(words_without_noises):
    c = collections.Counter(words_without_noises)
    return c.most_common()
