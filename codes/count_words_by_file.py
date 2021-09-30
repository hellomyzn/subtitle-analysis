import sys
import os

import count_words


def main():
    args = sys.argv
    words = []
    words_without_noises = []
    noises = []
    word_times = []

    file_path = count_words.get_path(args)
    file_name = os.path.split(file_path)[-1]

    words = count_words.extract_words(file_path, words)
    words_without_noises, noises = count_words.remove_noises(words, words_without_noises, noises)
    word_times = count_words.count_words(words_without_noises)
    count_words.export_csv(word_times, file_name)
    count_words.export_noises(noises, file_name)

if __name__ == "__main__":
    main()