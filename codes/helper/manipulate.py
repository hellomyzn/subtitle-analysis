import csv


def extract_words(file_path, words):
    try:
        with open(file_path) as f:
            for line in f:
                words.extend(line.split())
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
    return words_without_noises, noises

def remove_subject(words):
    removed_words = {}

    subjects_pronouns = ["i", "you", "he", "she", "it", "they", "this",  "that", "there",  "these", "those", "we", "im", "ive", "shes", "hes",  "youre", "thats", "theres", "theyre", "youll", "youd", "youve", "shell"]
    objects_pronouns =  ["me", "him", "her", "them", "us"]
    possessives_adjectives =  ["my", "your", "his", "its", "our", "their"]
    possessives_pronouns = ["mine", "yours", "hers" "yours", "ours", "theirs"]
    reflexive_pronoun = ["myself", "yourself", "himself", "herself", "itself", "ourselves", "yourselves", "themselves"]
    articles = ["a", "an", "the"]
    interjections = [ "ah", "aha", "aw", "awesome", "aww", "boy", "man", "bye", "cheers", "cool", "gosh", "eh", "hi", "ha", "hey", "hello", "hmm", "huh", "nope", "oh", "ok", "okay", "ow", "ouch", "please", "shh", "uh", "um", "well", "please", "wow", "yeah", "ooh", "heh", "whoa", "ahem", "mr", "dr", "uhhuh", "mm", "ugh", "mmhm", "la", "ew", "uhoh"]
    prepositions = ["about", "after", "around", "as", "at", "before", "between", "but", "by", "down", "for", "from", "in", "into", "like", "of", "off", "on", "outside", "over", "since", "than", "to", "under", "until", "up", "with", "without"]
    conjunction = ["if", "because", "even", "once", "only", "so", "then", "while", "and", "or"]
    interrogative = ["what", "whatever", "which", "whichever", "who", "whoever", "whom", "whomever", "whose", "whom", "whats", "where", "how", "whos"]
    be_verbs = ["be", "is", "are", "am", "was", "were", "wasnt", "isnt", "arent"]
    etc = ["yes", "no", "not"]
    names = ["rachel", "monica", "joey", "phoebe", "marcel", "ross", "carol", "susan", "janice", "paolo", "ben", "paul", "bob", "helen", "aah", "joeys"]
    

    remove_words = subjects_pronouns + objects_pronouns + possessives_adjectives + possessives_pronouns + reflexive_pronoun + articles + interjections + prepositions + conjunction + interrogative + be_verbs + etc + names

    for i in range(1, len(words) + 1):
        removed_words[str(i)] = [word for word in words[str(i)] if word[0] not in remove_words]
    return removed_words


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