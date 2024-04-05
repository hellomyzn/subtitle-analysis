"""services.frequency_service"""
#########################################################
# Builtin packages
#########################################################
from collections import Counter
from dataclasses import dataclass

#########################################################
# 3rd party packages
#########################################################
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

#########################################################
# Own packages
#########################################################
from common.decorator import exception_module
from models import Vocabulary
from models import Frequency
from repositories.frequencies import CsvFrequencyRepository
from repositories.frequencies import GssFrequencyRepository
from utils import has_file, make_file


@dataclass
class FrequencyService(object):
    """frequency service"""

    def __init__(self):
        self.csv_repo = CsvFrequencyRepository()
        self.gss_repo = GssFrequencyRepository()

    @exception_module
    def calculate_vocab_frequencies(self, vocabs: list[Vocabulary,]) -> list[Frequency, ]:
        vocabs = [vocab.english for vocab in vocabs]
        vocab_freqs = dict(Counter(vocabs).most_common())

        freqs = []
        id_ = 1
        for vocab, times in vocab_freqs.items():
            freq = Frequency(id=id_,
                             vocabulary=vocab,
                             times=times)
            freqs.append(freq)
            id_ += 1
        return freqs

    @exception_module
    def add(self, freqs: list[Frequency, ]):
        self.write_csv(freqs)
        self.write_gss(freqs)

    @exception_module
    def write_csv(self, freqs: list[Frequency, ], output_path: str | None = None) -> None:
        if output_path:
            path = self.csv_repo.path
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(freqs, path=output_path)

    @exception_module
    def write_gss(self, freqs: list[Frequency, ]) -> None:
        self.gss_repo.add(freqs)

    @exception_module
    def add_by_pos(self, vocabs: list[Vocabulary, ]) -> None:
        poss = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS",
                "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS",
                "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO",
                "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
                "WP", "WP$", "WRB"]
        for pos in poss:
            output_path = f"/pos/{pos}"
            vocabs_pos = self.__extract_by_pos(vocabs, pos)
            freqs_pos = self.calculate_vocab_frequencies(vocabs_pos)
            self.write_csv(freqs_pos, output_path=output_path)

    @staticmethod
    def __extract_by_pos(vocabularies: list[Vocabulary,], pos: str) -> list[Vocabulary,]:
        vocabs_pos = []
        for vocab in vocabularies:
            if vocab.pos == pos:
                vocabs_pos.append(vocab)

        return vocabs_pos

    @exception_module
    def add_result(self):
        funcs = {
            "verb": self.get_verbs,
            "adjective": self.get_adjectives,
            "adverb": self.get_adverbs,
            "noun": self.get_nouns}

        result_dict = {}
        for path, func in funcs.items():
            freqs = func()
            self.write_csv(freqs, output_path=path)
            for freq in freqs:
                vocab = freq.vocabulary
                times = int(freq.times)
                try:
                    result_dict[vocab] += times
                except KeyError:
                    result_dict[vocab] = times

        sorted_dict = dict(sorted(result_dict.items(),
                                  key=lambda freq: freq[1],
                                  reverse=True))
        freqs = self.__modelize_from_lemmatized_freqs(sorted_dict)

        self.write_csv(freqs, output_path="result")
        repo = GssFrequencyRepository(sheet_name="result")
        repo.add(freqs)

    @exception_module
    def get_verbs(self):
        poss = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        verbs = self.__get_lemmatized_freqs(poss, "v")
        return verbs

    @exception_module
    def get_adjectives(self):
        poss = ["JJ", "JJR", "JJS"]
        adjectives = self.__get_lemmatized_freqs(poss, "a")
        return adjectives

    @exception_module
    def get_adverbs(self):
        poss = ["RB", "RBR", "RBS", "RP"]
        adverbs = self.__get_lemmatized_freqs(poss, "r")
        return adverbs

    @exception_module
    def get_nouns(self):
        poss = ["NN", "NNS"]
        nowns = self.__get_lemmatized_freqs(poss, "n")
        return nowns

    def __get_lemmatized_freqs(self, poss: list[Frequency], mode: str) -> list[Frequency]:
        freqs_from_repo = self.get_by_poss(poss)
        freqs_lem = self.__lemmatize(freqs_from_repo, mode)
        freqs = self.__modelize_from_lemmatized_freqs(freqs_lem)
        return freqs

    @exception_module
    def get_by_poss(self, poss: list[str,]) -> list[Frequency]:
        freqs = []
        for pos in poss:
            freq_from_repo = self.get_by_pos(pos)
            freqs.extend(freq_from_repo)
        return freqs

    @exception_module
    def get_by_pos(self, pos: str) -> list[Frequency, ]:
        freqs = self.csv_repo.get_by_pos(pos)
        return freqs

    @staticmethod
    def __lemmatize(freqs: list[Frequency,], mode: str) -> dict[str, int]:
        dict_ = {}
        nltk.download('wordnet')
        lem = WordNetLemmatizer()

        for freq in freqs:
            vocab = freq.vocabulary
            times = int(freq.times)
            vocab_lem = lem.lemmatize(vocab, mode)
            try:
                dict_[vocab_lem] += times
            except KeyError:
                dict_[vocab_lem] = times

        sorted_dict = dict(sorted(dict_.items(),
                                  key=lambda freq: freq[1],
                                  reverse=True))
        return sorted_dict

    @staticmethod
    def __modelize_from_lemmatized_freqs(freqs_lem: dict[str: str],):
        freqs_list = []
        id_ = 1
        for vocab, times in freqs_lem.items():
            freq = Frequency(id=id_,
                             vocabulary=vocab,
                             times=times)
            freqs_list.append(freq)
            id_ += 1

        return freqs_list
