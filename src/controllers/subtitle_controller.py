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
        self.sub_serv.add(subs)

        vocabs = self.vocab_serv.extract_from_subtitles(subs)
        self.vocab_serv.add(vocabs)
        self.vocab_serv.add_by_pos(vocabs)

        freqs = self.freq_serv.calculate_vocab_frequencies(vocabs)
        self.freq_serv.add(freqs)
        self.freq_serv.add_by_pos(vocabs)

        self.freq_serv.add_result()
