"""services.phrasal_verb_service"""
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
from repositories.phrasal_verbs import CsvPhrasalVerbRepository
from repositories.phrasal_verbs import GssPhrasalVerbRepository
from utils import lemmatize_vocabulary, scrap_vocabulary


@dataclass
class PhrasalVerbService(object):
    """subtitle service"""

    def __init__(self):
        self.csv_repo = CsvPhrasalVerbRepository()
        self.gss_repo = GssPhrasalVerbRepository()

    @exception_module
    def add(self, subs: list[Vocabulary, ]) -> None:
        # TODO: put together csv and gss as list
        # not write csv since it's written on pos/VPV
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
        """
        Retrieve phrasal verbs from a list of Vocabulary objects.

        Exclusion criteria:
        - Exclude conjunctions after the verb (e.g., "know" in: "You probably didn't know this but back in high school I had a major crush on you.")
        - Exclude existential "there" after the verb (e.g., "That's like saying there is only one flavor of ice cream.")
        - Exclude verbs after the verb (e.g., "That's like saying there is only one flavor of ice cream.")
        - Exclude "IN" of "that" or "if" after the verb (e.g., "You still think you might want that fifth date.")
        - Exclude "to" (TO) (e.g., "I went to your building.")
        - Exclude "IN" of "if" after the verb (e.g., "I mean what if you get one woman and that's it.")

        Args:
            vocabs (list[Vocabulary]): List of Vocabulary objects to analyze.

        Returns:
            list[Phrase]: A list of Phrase objects representing the identified phrasal verbs.
        """
        info("retrieve phrasal verb")
        phrases = []
        id_ = 1
        verbs_to_exclude = ["be", "'m", "'re", "'ve", "am", "are", "is", "'s", "do"]
        for vocab in vocabs:
            # exclude aside from verbs and specific verbs
            if not vocab.is_verb() or vocab.original_form in verbs_to_exclude:
                continue

            # get vocabs after the verb in the same subtitle
            subtitle_vocabs = [v for v in vocabs if v.subtitle_id == vocab.subtitle_id]
            idx = subtitle_vocabs.index(vocab)
            vocabularies_after_verb = subtitle_vocabs[idx + 1:]

            # no need to analyze if there is no vocab after the verb
            if not vocabularies_after_verb:
                continue

            for next_vocab in vocabularies_after_verb:
                # it is not phrasal verb if word which might not phrasal verb comes after the verb
                if (next_vocab.is_coordinating_conjunction() or
                    next_vocab.is_existential_there() or
                    next_vocab.is_verb() or
                    next_vocab.word in ["if", "that"] or
                        next_vocab.pos in ["TO"]):
                    break

                # go to next if it is not preposition
                if not next_vocab.is_preposition():
                    continue

                phrasal_verb = " ".join([vocab.word, next_vocab.word])
                origin = lemmatize_vocabulary(vocab)
                phrasal_verb_origin = " ".join([origin, next_vocab.word])

                phrase = Vocabulary(
                    id=id_,
                    word=phrasal_verb,
                    meaning=None,
                    pos="VPV",
                    original_form=phrasal_verb_origin,
                    level=None,
                    eiken_level=None,
                    school_level=None,
                    toeic_level=None,
                    subtitle_id=vocab.subtitle_id)

                # Avoid scraping the same vocabulary by checking if it already exists
                existing_vocab = phrase.find_by_attr(phrases, "original_form")

                if existing_vocab:
                    phrase.level = existing_vocab.level
                    phrase.eiken_level = existing_vocab.eiken_level
                    phrase.school_level = existing_vocab.school_level
                    phrase.toeic_level = existing_vocab.toeic_level
                    phrase.meaning = existing_vocab.meaning
                else:
                    phrase.level, phrase.eiken_level, phrase.school_level, phrase.toeic_level, phrase.meaning = scrap_vocabulary(
                        phrase)

                # there is no meaning, it's not phrasal verb
                if phrase.meaning:
                    phrases.append(phrase)
                    id_ += 1

                # Stop after finding the first preposition. (e.g. go with: You're going out with a guy)
                break
        info("retrieved phrasal verb: {0}", len(phrases))
        return phrases
