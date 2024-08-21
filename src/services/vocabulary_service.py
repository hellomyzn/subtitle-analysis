"""services.vocabulary_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass
import requests

#########################################################
# 3rd party packages
#########################################################
import bs4
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
        """
        Adds a list of Vocabulary objects by writing them to both a CSV file and Google Sheets.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to be added.
        """
        self.write_csv(vocabs)
        self.write_gss(vocabs)

    @ exception_module
    def extract_from_subtitles(self, subs: list[Subtitle, ]):
        """
        Extracts vocabulary from subtitles using the NLTK package.

        Args:
            subs (list[Subtitle]): A list of English subtitles.

        Returns:
            list[Vocabulary]: A list of Vocabulary objects created from the subtitles.
        """
        # Download necessary NLTK resources
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

        vocabularies = []
        vocs_to_exclude = [".", ",", ":", "``", "''", "?", "!", "...", "[", "]", "&"]
        id_ = 1

        for sub in subs:
            # Tokenize the sentence into words
            words = nltk.word_tokenize(sub.sentence)
            # Tag each word with its part of speech
            tagged_words = nltk.pos_tag(words)

            for word, pos in tagged_words:
                word = word.lower()

                # Skip excluded vocabulary
                if word in vocs_to_exclude:
                    continue

                vocabulary = Vocabulary(
                    id=id_,
                    word=word,
                    meaning=None,
                    pos=pos,
                    original_form=None,
                    level=None,
                    eiken_level=None,
                    school_level=None,
                    toeic_level=None,
                    subtitle_id=sub.id)

                # Lemmatize to get the original form (e.g., studied -> study)
                origin = VocabularyService.__lemmatize(vocabulary)
                vocabulary.original_form = origin

                # Avoid scraping the same vocabulary by checking if it already exists
                existing_vocab = vocabulary.find_by_attr(vocabularies, "word")

                if existing_vocab:
                    vocabulary.level = existing_vocab.level
                    vocabulary.eiken_level = existing_vocab.eiken_level
                    vocabulary.school_level = existing_vocab.school_level
                    vocabulary.toeic_level = existing_vocab.toeic_level
                    vocabulary.meaning = existing_vocab.meaning
                else:
                    vocabulary.level, vocabulary.eiken_level, vocabulary.school_level, vocabulary.toeic_level, vocabulary.meaning = self.__scrap_vocabulary(
                        vocabulary)

                vocabularies.append(vocabulary)
                id_ += 1
        return vocabularies

    @classmethod
    def __lemmatize(cls, vocab: Vocabulary) -> str:
        """
        Get the original form (lemma) of the vocabulary.
        For example, 'studied' -> 'study'.
        This works only for verbs, adjectives, adverbs, and nouns.

        Args:
            vocab (Vocabulary): The vocabulary object containing the word to lemmatize.

        Returns:
            str: The original (lemmatized) form of the vocabulary, or the word itself if no lemmatization is possible.
        """
        lem = WordNetLemmatizer()
        word = vocab.word
        pos_map = {
            "v": vocab.is_verb,
            "a": vocab.is_adjective,
            "r": vocab.is_adverb,
            "n": vocab.is_noun
        }

        for mode, check_func in pos_map.items():
            if check_func():
                return lem.lemmatize(word, mode)

        return word

    @ exception_module
    def write_csv(self, vocabs: list[Vocabulary, ], output_path: str | None = None) -> None:
        """
        Writes a list of Vocabulary objects to a CSV file.
        If an output path is provided, the CSV will be saved to that location with a modified filename.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to write to the CSV file.
            output_path (str | None): Optional; If provided, this path will be used for the output CSV file.

        Returns:
            None
        """
        path = self.csv_repo.path

        if output_path:
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(vocabs, path=output_path)

    @ exception_module
    def write_gss(self, vocabs: list[Vocabulary, ]) -> None:
        """
        Writes a list of Vocabulary objects to Google Sheets.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to add to Google Sheets.

        Returns:
            None
        """
        self.gss_repo.add(vocabs)

    @ exception_module
    def sort_by_pos(self, vocabs: list[Vocabulary, ]) -> PartOfSpeech:
        """
        Sorts a list of Vocabulary objects by their part of speech and groups them into a PartOfSpeech object.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to sort.

        Returns:
            PartOfSpeech: An object containing the grouped Vocabulary objects by their part of speech.
        """
        pos = PartOfSpeech()
        for vocab in vocabs:
            pos.append_values(vocab.pos, vocab)
        return pos

    @ exception_module
    def add_by_pos(self, part_of_speech: PartOfSpeech) -> None:
        """
        Adds Vocabulary objects grouped by their part of speech to CSV files.

        Args:
            part_of_speech (PartOfSpeech): An object containing Vocabulary objects grouped by part of speech.

        Returns:
            None
        """
        for pos in part_of_speech.attributes:
            vocabs = part_of_speech.get_values(pos)
            output_path = f"/pos/{pos}"
            self.write_csv(vocabs, output_path=output_path)

    @exception_module
    def retrieve_phrasal_verbs(self, vocabs: list[Vocabulary, ]) -> list[Phrase, ]:
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

                phrasal_verb, origin = VocabularyService.__create_phrases_with_origin([vocab, next_vocab])
                phrases.append(Phrase(id=id_, phrase=phrasal_verb,
                                      original_form=origin,
                                      subtitle_id=vocab.subtitle_id))
                id_ += 1

                # Stop after finding the first preposition. (e.g. go with: You're going out with a guy)
                break
        print(len(phrases))
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
            subtitle_vocabs = [v for v in vocabs if v.subtitle_id == vocab.subtitle_id]
            idx = VocabularyService.__get_index_number(subtitle_vocabs, vocab)
            if idx is None:
                continue
            next_vocab = VocabularyService.__get_value_by_idx(subtitle_vocabs, idx+1)
            # if there is not next vocabulary, it's not group preposition
            if next_vocab is None:
                continue
            # if the next vocab comes from different subtitle, it is not group preposition
            if not vocab.subtitle_id == next_vocab.subtitle_id:
                continue

            # case A
            if any([vocab.is_adverb(),
                    vocab.is_adjective(),
                    vocab.is_conjunction(),
                    vocab.pos in ["VBG"]]):
                # exceptional case
                if vocab.word in ["going"]:
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
            if not vocab.subtitle_id == second_vocab.subtitle_id:
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
                                subtitle_id=vocab.subtitle_id)
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

        vocabs_list = [vocab.word for vocab in vocabs]
        phrase = " ".join(vocabs_list)

        origin = VocabularyService.__lemmatize(vocabs[idx])
        if origin:
            vocabs_list[idx] = origin
            origin = " ".join(vocabs_list)
        return phrase, origin

    @staticmethod
    def __scrap_vocabulary(vocab: Vocabulary) -> tuple[str | None, str | None, str | None, str | None, str | None]:
        """
        Scrapes Weblio to retrieve vocabulary levels and meaning.

        Args:
            vocab (Vocabulary): The vocabulary object containing the word to scrape.

        Returns:
            tuple[str | None, str | None, str | None, str | None, str | None]:
            A tuple containing level, Eiken level, school level, TOEIC level, and meaning.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/78.0.3904.97 Safari/537.36"
            )
        }
        word = vocab.original_form if vocab.original_form else vocab.word
        url = f'https://ejje.weblio.jp/content/{word}'

        html = requests.get(url, headers=headers, timeout=5)
        soup = bs4.BeautifulSoup(html.content, "html.parser")
        # Level keys
        level_keys = {
            "レベル": None,
            "英検": None,
            "学校レベル": None,
            "TOEIC® L&Rスコア": None
        }

        # Extract levels
        labels = soup.select(".learning-level-label")
        contents = soup.select(".learning-level-content")
        for label, content in zip(labels, contents):
            label_text = label.text.strip()
            if label_text in level_keys:
                level_keys[label_text] = content.text.strip()

        level = level_keys["レベル"]
        eiken = level_keys["英検"]
        school = level_keys["学校レベル"]
        toeic = level_keys["TOEIC® L&Rスコア"]

        # Extract meaning
        meaning_element = soup.select_one(".content-explanation")
        meaning = meaning_element.text.strip() if meaning_element else None

        return level, eiken, school, toeic, meaning
