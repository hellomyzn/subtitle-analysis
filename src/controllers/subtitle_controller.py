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
from services import PhrasalVerbService
from services import GroupPrepositionService
from services import FrequencyService


@dataclass
class SubtitleController(object):
    """subtitle controller"""

    def __init__(self):
        self.sub_serv = SubtitleService()
        self.vocab_serv = VocabularyService()
        self.phrasal_verb_serv = PhrasalVerbService()
        self.group_preposition_serv = GroupPrepositionService()
        self.freq_serv = FrequencyService()

    def add(self):
        """analyze vocabularies from subtitles and add to repository
        """
        subs = self.sub_serv.get_from_srt()
        self.sub_serv.add(subs)

        vocabs = self.vocab_serv.extract_from_subtitles(subs)
        self.vocab_serv.add(vocabs)

        pos_vocabs = self.vocab_serv.sort_by_pos(vocabs)

        phrasal_verbs = self.phrasal_verb_serv.retrieve_from_vocabularies(vocabs)
        pos_vocabs.VPV = phrasal_verbs
        self.phrasal_verb_serv.add(phrasal_verbs)

        group_prepositions = self.group_preposition_serv.retrieve_from_vocabularies(vocabs)
        pos_vocabs.GP = group_prepositions
        self.group_preposition_serv.add(group_prepositions)

        self.vocab_serv.add_by_pos(pos_vocabs)

        freqs = self.freq_serv.calculate_vocab_frequencies(vocabs)
        self.freq_serv.add(freqs)
        self.freq_serv.add_by_pos(pos_vocabs)

        verbs = [v for v in vocabs if v.is_verb()]
        verbs_freq = self.freq_serv.calculate_vocab_frequencies(verbs)
        self.freq_serv.add(freqs=verbs_freq, csv_filename="verbs")

        adverbs = [v for v in vocabs if v.is_adverb()]
        adverbs_freq = self.freq_serv.calculate_vocab_frequencies(adverbs)
        self.freq_serv.add(freqs=adverbs_freq, csv_filename="adverbs")

        adjectives = [v for v in vocabs if v.is_adjective()]
        adjectives_freq = self.freq_serv.calculate_vocab_frequencies(adjectives)
        self.freq_serv.add(freqs=adjectives_freq, csv_filename="adjectives")

        nouns = [v for v in vocabs if v.is_noun()]
        noun_freq = self.freq_serv.calculate_vocab_frequencies(nouns)
        self.freq_serv.add(freqs=noun_freq, csv_filename="nouns")

        all_vocabs = verbs + adverbs + adjectives + nouns
        all_freqs = self.freq_serv.calculate_vocab_frequencies(all_vocabs)
        self.freq_serv.add(all_freqs, csv_filename="result")
