import sys
import os
import csv

from helper import calculate
from helper import manipulate
from helper import system


def main():
    all_words = []
    all_word_and_times = []
    line = "\n***********************************************************************\n"

    # get folder path
    words_folder_path = "./data/words/"

    # get files in the folder
    words_files = system.get_files_name(words_folder_path)

    # get words from files
    for file in words_files:
        file_path = words_folder_path + file
        all_words.extend(manipulate.import_txt(file_path))

    all_word_and_times = calculate.count_words(all_words)

    # system.make_dir("./data/", "all-words")
    manipulate.export_csv(all_word_and_times, "word_and_times", "all-words")
    words_by_frequency = calculate.count_words_by_frequency(10, all_word_and_times)

    print(line + "START:    " + "word_and_times")
    print("ALL:      " + str(len(all_word_and_times)))
    for frequency, data in words_by_frequency.items():
        percentage = calculate.percentage_of_words(len(all_word_and_times), len(data))
        print(frequency + ":        " + str(len(data)) + " (" + str(percentage) + ")" )
    print("DONE:    " + "word_and_times" + line)


    print(line + "START:    " + "words")
    print("ALL:      " + str(len(all_words)))
    for frequency, data in words_by_frequency.items():
        times = 0
        for k, v in data:
            times += v
        percentage = calculate.percentage_of_words(len(all_words), times)
        print(frequency + ":        " + str(times) + " (" + str(percentage) + ")" )
    print("DONE:    " + "words" + line)

if __name__ == "__main__":
    main()