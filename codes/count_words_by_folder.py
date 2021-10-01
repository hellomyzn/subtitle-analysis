from helper import calculate
from helper import manipulate
from helper import system


def main():
    files = []
    all_words = []
    line = "\n***********************************************************************\n"

    folder_path = system.get_args(1)
    files = system.get_files_name(folder_path)
    system.make_dir("./data/", "word_and_times")
    system.make_dir("./data/", "words")
    system.make_dir("./data/", "noises")

    for file in files:
        words = []
        words_without_noises = []
        noises = []
        word_times = []
        file_path = folder_path + file

        print(line + "START:                " + file)

        words = manipulate.extract_words(file_path, words)
        words_without_noises, noises = manipulate.remove_noises(words, words_without_noises, noises)
        all_words.extend(words_without_noises)

        word_times = calculate.count_words(words_without_noises)
        manipulate.export_csv(word_times, file, "word_and_times")
        manipulate.export_txt(noises, file, "noises")
        manipulate.export_txt(words_without_noises, file, "words")
        print("DONE:                 " + file + line)

    print(line + "START:                all-words")
    print("ALL-WORDS:            " + str(len(all_words)))
    print("DONE:                 all-words" + line)

if __name__ == "__main__":
    main()