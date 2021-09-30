import sys

import collections


def main():
    args = sys.argv
    words = []
    words_without_noise = []
    noise = []

    file_path = get_file_path(args)
    extract_words(file_path, words)
    remove_noise(words, words_without_noise, noise)
    count_words(words_without_noise)

def get_file_path(args):
    try:
        return args[1]
    except:
        print(str.upper("***   choose file which you want to try   ***"))
        exit()


def extract_words(file_path, words):
    try:
        with open(file_path) as f:
            for line in f:
                words.extend(line.split())
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
        
def count_words(words_without_noise):
    c = collections.Counter(words_without_noise)
    print(c.items())

if __name__ == "__main__":
    main()