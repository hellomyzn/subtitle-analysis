import collections
import csv
import glob

def get_path(args):
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


def get_files_name(folder_path):
    files = glob.glob(folder_path + "/*")
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


def export_csv(word_times, file_name):
    file_name = file_name + ".csv"
    with open("./csvs/" + file_name, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(word_times)


def export_noises(noises, file_name):
    file_name = file_name + "-noise.csv"
    with open("./noises/" + file_name, "w") as f:
        f.write('\n'.join(noises))