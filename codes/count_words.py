import collections
import csv

def get_file_path(args):
    try:
        return args[1]
    except:
        print(str.upper("***   choose file which you want to try   ***"))
        exit()

def get_file_name(args):
    try:
        return args[2]
    except:
        print(str.upper("***   file name is not difined   ***"))

def extract_words(file_path, words):
    try:
        with open(file_path) as f:
            for line in f:
                words.extend(line.split())
        return words
    except:
        print(str.upper("***   wrong file path   ***"))
        exit()


def remove_noise(words, words_without_noise, noise):
    words = [word.replace("'", '') for word in words]
    words = [word.replace('"', '') for word in words]
    words = [word.replace(":", '') for word in words]
    words = [word.replace(",", '') for word in words]
    words = [word.replace(".", '') for word in words]
    words = [word.replace("?", '') for word in words]
    words = [word.replace("!", '') for word in words]
    words = [word.replace("-", '') for word in words]
    words = [word.replace(">", '') for word in words]
    words = [word.replace("[", '') for word in words]
    words = [word.replace("]", '') for word in words]

    for word in words:
        # remove except Alphabet
        if word.isalpha():
            words_without_noise.append(str.lower(word))
        else:
            noise.append(word)
    return words_without_noise, noise
        

def count_words(words_without_noise):
    c = collections.Counter(words_without_noise)
    return c.most_common()


def export_csv(word_times, file_name):
    file_name = file_name + ".csv"
    with open("../csvs/" + file_name, "w", encoding="Shift_jis") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(word_times)