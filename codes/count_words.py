import sys
import os

import collections
import csv
import glob


def get_args(num):
    args = sys.argv
    try:
        return args[num]
    except:
        print(str.upper("***   choose file which you want to try   ***"))
        exit()


def get_files_name(folder_path):
    files = []
    for f in glob.glob(folder_path + "/*"):
        files.append(os.path.split(f)[-1])

    return files


def extract_words(file_path, words):
    try:
        with open(file_path) as f:
            for line in f:
                words.extend(line.split())

            print("WORDS:                " + str(len(words)))
        return words
    except:
        print(str.upper("***   wrong file path   ***"))
        exit()

def make_dir(path):
    folder_path = "./data/"
    os.mkdir(folder_path + path)


def remove_noises(words, words_without_noises, noises):
    words = [word.replace("'", '') for word in words]
    words = [word.replace('"', '') for word in words]
    words = [word.replace(":", '') for word in words]
    words = [word.replace(",", '') for word in words]
    words = [word.replace(".", '') for word in words]
    words = [word.replace("/", '') for word in words]
    words = [word.replace("?", '') for word in words]
    words = [word.replace("!", '') for word in words]
    words = [word.replace("-", '') for word in words]
    words = [word.replace(">", '') for word in words]
    words = [word.replace("[", '') for word in words]
    words = [word.replace("]", '') for word in words]

    for word in words:
        # remove except Alphabet
        if word.isalpha():
            words_without_noises.append(str.lower(word))
        else:
            noises.append(word)

    print("NOISES:               " + str(len(noises)))
    print("WORDS_WITHOUT_NOISES: " + str(len(words_without_noises)))
    return words_without_noises, noises
        

def count_words(words_without_noises):
    c = collections.Counter(words_without_noises)
    return c.most_common()


def export_csv(word_times, file_name, folder_path):
    file_name = file_name + ".csv"
    with open("./data/" + folder_path + "/" + file_name, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(word_times)


def export_noises(noises, file_name):
    file_name = file_name + "-noise.csv"
    with open("./noises/" + file_name, "w") as f:
        f.write('\n'.join(noises))