import sys

import collections
import csv



def main():
    args = sys.argv
    words = []
    words_without_noise = []
    noise = []
    words_times = []

    file_path = get_file_path(args)
    extract_words(file_path, words)
    remove_noise(words, words_without_noise, noise)
    words_times = count_words(words_without_noise)
    export_csv(words_times)

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
    return c.most_common()


def export_csv(words_times):
    with open("stock.csv", "w", encoding="Shift_jis") as f: # 文字コードをShift_JISに指定
        writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
        writer.writerows(words_times) # csvファイルに書き込み

if __name__ == "__main__":
    main()