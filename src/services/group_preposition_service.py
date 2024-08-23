"""services.group_preposition_service"""
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
from common.decorator import exception_module
from common.log import info
from models import Vocabulary
from repositories.group_prepositions import CsvGroupPrepositionRepository
from repositories.group_prepositions import GssGroupPrepositionRepository
from utils import lemmatize_vocabulary, scrap_vocabulary, get_index_number, get_value_by_idx


@dataclass
class GroupPrepositionService(object):
    """group preposition service"""

    def __init__(self):
        self.csv_repo = CsvGroupPrepositionRepository()
        self.gss_repo = GssGroupPrepositionRepository()

    @exception_module
    def add(self, subs: list[Vocabulary, ]) -> None:
        # TODO: put together csv and gss as list
        # not write csv since it's written on pos/GP
        # self.write_csv(subs)
        self.write_gss(subs)

    @exception_module
    def write_csv(self, subs: list[Vocabulary, ]) -> None:
        """write subtitle on csv

        Args:
            subs (list[Subtitle, ]): subtitles
        """
        self.csv_repo.write(subs)

    @exception_module
    def write_gss(self, subs: list[Vocabulary, ]) -> None:
        """write subtitle on gss

        Args:
            subs (list[Subtitle, ]): subtitles
        """
        self.gss_repo.add(subs)

    @exception_module
    def retrieve_from_vocabularies(self, vocabs: list[Vocabulary, ]) -> list[Vocabulary, ]:
        """retrieve group preposition
            e.g.
                case A:
                    - adverb + preposition
                        To the point of - "He was angry to the point of yelling."
                    - adjective + preposition
                        Contrary to expectations, the weather remained pleasant throughout the weekend.
                    - conjunction + preposition
                        The road was blocked because of a traffic accident.
                    - according(VBG) to
                        To the point of - "He was angry to the point of yelling."
                case B:
                    - preposition + noun + preposition
                        We’ll extend the deadline in light of your request.
                    - to the point of:
                        He was angry to the point of yelling.
                case C:
                    - adverb + adverb + preposition (as far as)
                        As far as I know, she’s still living in New York.

            exceptional case
                - going(VBG) to(TO)

        Args:
            vocabs (list[Vocabulary, ]): vocabularies

        Returns:
            list[Phrase, ]: phrases
        """

        info("retrieve group preposition")
        id_ = 1
        phrases = []
        for vocab in vocabs:
            is_modelize = False

            # Get the next vocab(s) in the same subtitle
            subtitle_vocabs = [v for v in vocabs if vocab.is_same_value(v, "subtitle_id")]
            idx = get_index_number(subtitle_vocabs, vocab)
            if idx is None:
                continue

            next_vocab: Vocabulary = get_value_by_idx(subtitle_vocabs, idx+1)
            second_vocab: Vocabulary = get_value_by_idx(subtitle_vocabs, idx+2)
            # if there is not next vocabulary, it's not group preposition
            # if the next vocab comes from different subtitle, it is not group preposition
            if (next_vocab is None or
                    not vocab.is_same_value(next_vocab, "subtitle_id")):
                continue

            # Case A: adverb/adjective/conjunction + preposition
            if (any([vocab.is_adverb(), vocab.is_adjective(), vocab.is_conjunction(), vocab.pos in ["VBG"]]) and
                    next_vocab.is_preposition()):

                # exceptional case
                if vocab.word in ["going"]:
                    continue

                is_modelize = True
                group_preposition, group_preposition_origin = self.__lemmatize_and_create_phrase(vocab, next_vocab)
            # Case B: preposition + (noun) + preposition
            elif vocab.is_preposition():
                if next_vocab.pos in ["DT"]:
                    next_vocab = get_value_by_idx(subtitle_vocabs, idx+2)
                    second_vocab = get_value_by_idx(subtitle_vocabs, idx+3)
                if (second_vocab and
                        all([next_vocab.is_noun(), second_vocab.is_preposition()])):
                    is_modelize = True
                    group_preposition, group_preposition_origin = self.__lemmatize_and_create_phrase(
                        vocab, next_vocab, second_vocab)

            # Case C: adverb + adverb + preposition
            if (second_vocab and
                    all([vocab.is_adverb(), next_vocab.is_adverb(), second_vocab.is_preposition()])):
                is_modelize = True
                group_preposition, group_preposition_origin = self.__lemmatize_and_create_phrase(
                    vocab, next_vocab, second_vocab)

            # modelize
            if is_modelize:
                group_preposition = Vocabulary(
                    id=id_,
                    word=group_preposition,
                    meaning=None,
                    pos="GP",
                    original_form=group_preposition_origin,
                    level=None,
                    eiken_level=None,
                    school_level=None,
                    toeic_level=None,
                    subtitle_id=vocab.subtitle_id)

                # Avoid scraping the same vocabulary by checking if it already exists
                existing_vocab = group_preposition.find_by_attr(phrases, "original_form")

                if existing_vocab:
                    group_preposition.level = existing_vocab.level
                    group_preposition.eiken_level = existing_vocab.eiken_level
                    group_preposition.school_level = existing_vocab.school_level
                    group_preposition.toeic_level = existing_vocab.toeic_level
                    group_preposition.meaning = existing_vocab.meaning
                else:
                    group_preposition.level, group_preposition.eiken_level, group_preposition.school_level, group_preposition.toeic_level, group_preposition.meaning = scrap_vocabulary(
                        group_preposition.word)

                # there is no meaning, it's not phrasal verb
                if group_preposition.meaning:
                    phrases.append(group_preposition)
                    id_ += 1
        info("retrieved group preposition: {0}", len(phrases))
        return phrases

    @staticmethod
    def __lemmatize_and_create_phrase(vocab: Vocabulary, *next_vocabs: list[Vocabulary]):
        # Get the next vocab(s) in the same subtitle
        words = [vocab.word] + [v.word for v in next_vocabs]

        target = vocab
        if len(next_vocabs) == 2:
            target = next_vocabs[0]

        origin = lemmatize_vocabulary(target)

        origin_words = [origin] + [v.word for v in next_vocabs]
        if len(next_vocabs) == 2:
            origin_words[0] = vocab.word
            origin_words[1] = origin

        return " ".join(words), " ".join(origin_words)
