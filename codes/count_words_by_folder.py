import count_words


def main():
    files = []
    all_words = []
    line = "\n***********************************************************************\n"

    folder_path = count_words.get_args(1)
    files = count_words.get_files_name(folder_path)
    count_words.make_dir("word_and_times")
    count_words.make_dir("words")
    count_words.make_dir("noises")

    for file in files:
        words = []
        words_without_noises = []
        noises = []
        word_times = []
        file_path = folder_path + file

        print(line + "START:                " + file)

        words = count_words.extract_words(file_path, words)
        words_without_noises, noises = count_words.remove_noises(words, words_without_noises, noises)
        all_words.extend(words_without_noises)

        word_times = count_words.count_words(words_without_noises)
        count_words.export_csv(word_times, file, "word_and_times")
        count_words.export_txt(noises, file, "noises")
        print("DONE:                 " + file + line)

    print(line + "START:                all-words")
    all_word_times = count_words.count_words(all_words)
    # count_words.export_csv(all_word_times, "all-words")
    print("ALL-WORDS:            " + str(len(all_words)))
    print("DONE:                 all-words" + line)

if __name__ == "__main__":
    main()