import csv


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


def export_csv(word_times, file_name, folder_path):
    file_name = file_name + ".csv"
    with open("./data/" + folder_path + "/" + file_name, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(word_times)


def import_txt(file_path):
    words = []
    with open(file_path, "r") as f:
        for line in f:
            words += line.split()
    return words


def export_txt(noises, file_name, folder_path):
    file_name = file_name + ".txt"
    with open("./data/" + folder_path + "/" + file_name, "w") as f:
        f.write('\n'.join(noises))