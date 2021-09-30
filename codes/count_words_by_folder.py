import sys
import os

import count_words


def main():
    args = sys.argv
    files = []
    line = "\n***********************************************************************\n"

    folder_path = count_words.get_path(args)
    files = count_words.get_files_name(folder_path)

    for file in files:
        words = []
        words_without_noises = []
        noises = []
        word_times = []

        file_path = file
        file_name = os.path.split(file_path)[-1]
        print(line + "START:                " + file_name)

        words = count_words.extract_words(file_path, words)
        words_without_noises, noises = count_words.remove_noises(words, words_without_noises, noises)
        word_times = count_words.count_words(words_without_noises)
        count_words.export_csv(word_times, file_name)
        count_words.export_noises(noises, file_name)
        print("DONE:                 " + file_name + line)

if __name__ == "__main__":
    main()