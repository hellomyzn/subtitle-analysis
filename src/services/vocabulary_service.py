"""services.vocabulary_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

#########################################################
# Own packages
#########################################################
from common.decorator import exception_module
from models import Subtitle
from models import Vocabulary
from models import PartOfSpeech
from models import Phrase
from repositories.vocabularies import CsvVocabularyRepository
from repositories.vocabularies import GssVocabularyRepository
from utils import has_file, make_file


@ dataclass
class VocabularyService(object):
    """vocabulary service"""

    def __init__(self):
        self.csv_repo = CsvVocabularyRepository()
        self.gss_repo = GssVocabularyRepository()

    @ exception_module
    def add(self, vocabs: list[Vocabulary, ]):
        self.write_csv(vocabs)
        self.write_gss(vocabs)

    @ exception_module
    def extract_from_subtitles(self, subs: list[Subtitle, ]):
        """extract vocabulary from sentence using nltk package

        Args:
            subs (list): english subtitles

        Returns:
            list[Vocabulary,]: vocabularies splitted by nltk
        """
        # download necessary sources
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

        vocabularies = []
        vocs_to_exclude = [".", ",", ":", "``", "''", "?", "!", "...", "[", "]"]
        id_ = 1

        for sub in subs:
            # separate sentence by word
            morph = nltk.word_tokenize(sub.sentence)
            # analyze part of speech by word
            voc_pos_list = nltk.pos_tag(morph)
            for voc, pos in voc_pos_list:
                voc = voc.lower()

                # if vocabulary is not word
                if voc in vocs_to_exclude:
                    continue

                vocabulary = Vocabulary(id=id_, english=voc, pos=pos,
                                        original=None, subject_id=sub.id)
                # get original form
                # e.g. studied -> study
                origin = VocabularyService.__lemmatize(vocabulary)
                vocabulary.original = origin

                vocabularies.append(vocabulary)
                id_ += 1
        return vocabularies

    @classmethod
    def __lemmatize(cls, vocab: Vocabulary) -> str:
        """get original form of vocabulary
            e.g. studied -> study
            it works to only verb, adjective, adverb, noun.

        Args:
            vocab (Vocabulary): vocabulary

        Returns:
            str: original form of vocabulary
        """
        lem = WordNetLemmatizer()
        word = vocab.english
        origin = None
        mode = None

        if vocab.is_verb():
            mode = "v"
        if vocab.is_adjective():
            mode = "a"
        if vocab.is_adverb():
            mode = "r"
        if vocab.is_noun():
            mode = "n"

        if mode:
            origin = lem.lemmatize(word, mode)
        return origin

    @ exception_module
    def write_csv(self, vocabs: list[Vocabulary, ], output_path: str | None = None) -> None:
        if output_path:
            path = self.csv_repo.path
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(vocabs, path=output_path)

    @ exception_module
    def write_gss(self, vocabs: list[Vocabulary, ]) -> None:
        self.gss_repo.add(vocabs)

    @ exception_module
    def sort_by_pos(self, vocabs: list[Vocabulary, ]) -> PartOfSpeech:
        pos = PartOfSpeech()
        for vocab in vocabs:
            pos.append_values(vocab.pos, vocab)
        return pos

    @ exception_module
    def add_by_pos(self, part_of_speech: PartOfSpeech) -> None:
        poss = part_of_speech.attributes
        for pos in poss:
            vocabs = part_of_speech.get_values(pos)
            output_path = f"/pos/{pos}"
            self.write_csv(vocabs, output_path=output_path)

    @exception_module
    def retrieve_phrasal_verbs(self, vocabs: list[Vocabulary, ]) -> list[Phrase, ]:
        """retrieve phrasal verbs

            exclude conjunction after verb
                e.g. know in: you probably didn't know this but back in high school I had a major crush on you.
            exclude existential there after verb
                e.g. That's like saying there is only one flavor of ice cream.
            exclude verb after verb
                e.g. That's like saying there is only one flavor of ice cream.
            exclude IN of that, if after verb
                e.g. You still think you might want that(IN) fifth date
            exclude to(TO)
                e.g. I went to your building.
            exclude IN of if after verb
                e.g. I mean what if(IN) you get one woman and that's it.

        Args:
            vocabs (list[Vocabulary, ]): _description_

        Returns:
            phrases (list[Phrase, ]): _description_
        """
        phrases = []
        id_ = 1
        verbs_to_exclude = ["be", "'m", "'re", "'ve", "am", "are", "is", "'s", "do"]
        for vocab in vocabs:
            # exclude aside from verbs and specific verbs
            if any([not vocab.is_verb(),
                    vocab.original in verbs_to_exclude]):
                continue

            # get vocabs after the verb in the same subtitle
            subtitle_vocabs = [v for v in vocabs if v.subject_id == vocab.subject_id]
            idx = subtitle_vocabs.index(vocab)
            vocabularies_after_verb = subtitle_vocabs[idx + 1:]

            # no need to analyze if there is no vocab after the verb
            if vocabularies_after_verb == []:
                continue

            for vav in vocabularies_after_verb:
                # it is not phrasal verb if word which might not phrasal verb comes after the verb
                if any([vav.is_coordinating_conjunction(),
                        vav.is_existential_there(),
                        vav.is_verb(),
                        vav.english in ["if", "that"],
                        vav.pos in ["TO"]]):
                    break

                # go to next if it is not preposition
                if not vav.is_preposition():
                    continue

                phrasal_verb, origin = VocabularyService.__create_phrases_with_origin([vocab, vav])
                phrase = Phrase(id=id_, phrase=phrasal_verb,
                                original_form=origin,
                                subtitle_id=vocab.subject_id)
                id_ += 1
                phrases.append(phrase)

                # after find a preposition, no need to find the second preposition
                # e.g. go with: You're going out with a guy
                break
        return phrases

    def retrieve_group_preposition(self, vocabs: list[Vocabulary, ]) -> list[Phrase, ]:
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
        id_ = 1
        phrases = []
        for vocab in vocabs:
            is_modelize = False
            # get next vocab
            subtitle_vocabs = [v for v in vocabs if v.subject_id == vocab.subject_id]
            idx = VocabularyService.__get_index_number(subtitle_vocabs, vocab)
            if idx is None:
                continue
            next_vocab = VocabularyService.__get_value_by_idx(subtitle_vocabs, idx+1)
            # if there is not next vocabulary, it's not group preposition
            if next_vocab is None:
                continue
            # if the next vocab comes from different subtitle, it is not group preposition
            if not vocab.subject_id == next_vocab.subject_id:
                continue

            # case A
            if any([vocab.is_adverb(),
                    vocab.is_adjective(),
                    vocab.is_conjunction(),
                    vocab.pos in ["VBG"]]):
                # exceptional case
                if vocab.english in ["going"]:
                    continue

                if next_vocab.is_preposition():
                    is_modelize = True
                    group_preposition, origin = VocabularyService.__create_phrases_with_origin([vocab, next_vocab])

            # get second vocab
            second_vocab = VocabularyService.__get_value_by_idx(subtitle_vocabs, idx+2)
            # if there is not next vocabulary, it's not group preposition
            if second_vocab is None:
                continue
            # if the next vocab comes from different subtitle, it is not group preposition
            if not vocab.subject_id == second_vocab.subject_id:
                continue

            # case B
            if vocab.is_preposition():
                # in case of "To the point of
                # e.g:  "He was angry to the point of yelling."
                if next_vocab.pos in ["DT"]:
                    next_vocab = VocabularyService.__get_value_by_idx(subtitle_vocabs, idx+2)
                    second_vocab = VocabularyService.__get_value_by_idx(subtitle_vocabs, idx+3)
                if second_vocab is None:
                    continue

                if all([next_vocab.is_noun(),
                        second_vocab.is_preposition()]):
                    is_modelize = True
                    group_preposition, origin = VocabularyService.__create_phrases_with_origin(
                        [vocab, next_vocab, second_vocab])

            # case C
            if all([vocab.is_adverb(),
                    next_vocab.is_adverb(),
                    second_vocab.is_preposition()]):
                is_modelize = True
                group_preposition, origin = VocabularyService.__create_phrases_with_origin(
                    [vocab, next_vocab, second_vocab])

            # modelize
            if is_modelize:
                phrase = Phrase(id=id_, phrase=group_preposition,
                                original_form=origin,
                                subtitle_id=vocab.subject_id)
                id_ += 1
                phrases.append(phrase)

        return phrases

    @classmethod
    def __get_index_number(cls, list_: list, val) -> int | None:
        """check the value in the list.

        Args:
            list_ (list): list
            val (_type_): value

        Returns:
            int | None: if it has in the list, return index number, but return None
        """
        idx = None
        try:
            idx = list_.index(val)
        except ValueError:
            pass
        return idx

    @classmethod
    def __get_value_by_idx(cls, list_: list[Vocabulary, ], idx: int) -> Vocabulary | None:
        """get value from list by index number

        Args:
            list_ (list[Vocabulary, ]): list
            idx (int): index number

        Returns:
            Vocabulary | None: value. if it is IndexError, None
        """
        val = None
        try:
            val = list_[idx]
        except IndexError:
            pass
        return val

    @classmethod
    def __create_phrases_with_origin(cls, vocabs: list[Vocabulary, ]) -> tuple[str, str | None]:
        """create phrase by vocabularies

        Args:
            vocabs (list[Vocabulary, ]): vocabularies

        Returns:
            tuple[str, str | None]: phrase, original form phrase
        """
        # get original form
        # e.g. studied -> study
        if int(len(vocabs)) == 2:
            idx = 0
        else:
            idx = 1

        vocabs_list = [vocab.english for vocab in vocabs]
        phrase = " ".join(vocabs_list)

        origin = VocabularyService.__lemmatize(vocabs[idx])
        if origin:
            vocabs_list[idx] = origin
            origin = " ".join(vocabs_list)
        return phrase, origin
