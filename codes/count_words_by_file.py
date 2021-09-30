import sys

import collections
import csv

import count_words


def main():
    args = sys.argv
    words = []
    words_without_noise = []
    noise = []
    word_times = []

    file_path = count_words.get_file_path(args)
    file_name = count_words.get_file_name(args)

    words = count_words.extract_words(file_path, words)
    words_without_noise, noise = count_words.remove_noise(words, words_without_noise, noise)
    word_times = count_words.count_words(words_without_noise)
    count_words.export_csv(word_times, file_name)

if __name__ == "__main__":
    main()