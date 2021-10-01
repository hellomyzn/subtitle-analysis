import sys
import os
import csv

from helper import calculate
from helper import manipulate
from helper import system


def main():
    words = []
    word_and_times = []

    # get folder path
    words_folder_path = "./data/words/"

    # get files in the folder
    words_files = system.get_files_name(words_folder_path)

    # get words from files
    for file in words_files:
        file_path = words_folder_path + file
        words.extend(manipulate.import_txt(file_path))

    word_and_times = calculate.count_words(words)

    # system.make_dir("./data/", "all-words")
    manipulate.export_csv(word_and_times, "word_and_times", "all-words")
    words_by_frequency = calculate.count_words_by_frequency(10, word_and_times)

    for (k,v) in words_by_frequency.items():
        percentage = calculate.percentage_of_words(len(word_and_times), len(v))
        print(k + ": " + str(len(v)) + " (" + str(percentage) + ")" )


if __name__ == "__main__":
    main()