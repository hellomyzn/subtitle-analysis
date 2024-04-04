"""controllers.subtitle_controller"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from services import SubtitleService
from services import VocabularyService
from services import FrequencyService


@dataclass
class SubtitleController(object):
    """subtitle controller"""

    def __init__(self):
        self.sub_serv = SubtitleService()
        self.vocab_serv = VocabularyService()
        self.freq_serv = FrequencyService()

    def add(self):
        """analyze vocabularies from subtitles and add to repository
        """
        subs = self.sub_serv.get_from_srt()
        self.sub_serv.write_csv(subs)

        vocabs = self.vocab_serv.extract_from_subtitles(subs)
        self.vocab_serv.write_csv(vocabs)

        freqs = self.freq_serv.calculate_vocab_frequencies(vocabs)
        self.freq_serv.write_csv(freqs)

        poss = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS",
                "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS",
                "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO",
                "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
                "WP", "WP$", "WRB"]
        for pos in poss:
            output_path = f"/pos/{pos}"
            pos_vocabs = self.vocab_serv.extract_by_pos(vocabs, pos)
            self.vocab_serv.write_csv(pos_vocabs, output_path=output_path)

            pos_freqs = self.freq_serv.calculate_vocab_frequencies(pos_vocabs)
            self.freq_serv.write_csv(pos_freqs, output_path=output_path)

        funcs = {
            "verb": self.freq_serv.get_verbs,
            "adjective": self.freq_serv.get_adjectives,
            "adverb": self.freq_serv.get_adverbs,
            "noun": self.freq_serv.get_nouns}

        total_freqs = []
        for path, func in funcs.items():
            freqs = func()
            total_freqs.extend(freqs)
            self.freq_serv.write_csv(freqs, output_path=path)

        sorted_total_freqs = sorted(total_freqs,
                                    key=lambda freq: freq.times,
                                    reverse=True)
        id_ = 1
        for freq in sorted_total_freqs:
            freq.id = id_
            id_ += 1

        self.freq_serv.write_csv(sorted_total_freqs, output_path="total")
